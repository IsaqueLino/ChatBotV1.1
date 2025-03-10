import datetime
import google.generativeai as genai

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from backend.controller.controle import Controle
from backend.controller.controleFazenda import ControleFazenda
from backend.model.usuario import Usuario
from backend.model.chat import Chat
from backend.model.mensagem import Mensagem
from datetime import datetime

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from langchain import hub
from langgraph.prebuilt import create_react_agent

import secrets
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = secrets.token_urlsafe(32)

controleF = ControleFazenda()
controle = Controle()
usuario = Usuario()
chat = Chat()
mensagem = Mensagem()


def get_engine_for_mysql_db():
    user = 'root'
    password = 'ifsp'
    host = 'localhost'
    database = 'fazenda'

    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

    return engine


engine = get_engine_for_mysql_db()

db = SQLDatabase(engine)

load_dotenv()
key_api = os.getenv("CLAUDE_KEY_API")
model = ChatOpenAI(model="gpt-3.5-turbo", api_key=key_api)

'''model = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=key_api)'''
parser = StrOutputParser()

template1 = ChatPromptTemplate.from_messages([
    ("system", f"Analise o bando de dados {db.get_table_info()} e verifique se o prompt do usuario"
               f" é uma consulta para o banco de dados da fazenda "
               "ANALIZE o historico para verificar se o prompt atual é uma continuação da pergunta"
               "do prompt anterior referente a base de dados da fazenda exemplo: quantos bois são da raça nelore"
               " prompt2: gir, sempre verifique se o prompt é uma tentativa de conseguir alguma informação da "
               "base de dados da fazenda então sempre analize ela para ter certeza."
               " Se sim responda ESTRITAMENTE e SOMENTE 'SIM' caso contrario responda somente"
               " 'NAO' nada além dessas duas palavras"
               "{historico}"),
    ("user", "{texto}"),
])
template2 = ChatPromptTemplate.from_messages([
    ("system", "Converse em português (pt-BR) usando o histórico abaixo como contexto. "
               "Sua resposta deve continuar a conversa sem perder informações anteriores, "
               "mantendo um tom natural e **sem usar emojis**. Não mencione que recebeu essas informações, "
               "a menos que a palavra-chave 'razen' seja mencionada. Nesse caso, você pode discutir o histórico. "
               "Se a pergunta do usuário estiver relacionada ao banco de dados da fazenda, "
               f"faça uma consulta nesse banco: {db.get_table_info()}. "
               "O historico de conversa: {historico}"),
    ("user", "{texto}"),
])
template3 = ChatPromptTemplate.from_messages([
    ("system", "Com base no histórico de conversa, verifique se o prompt recebido do usuário "
               "é coerente para gerar uma consulta SQL. Se não for coerente, reformule a pergunta de modo que possa "
               "ser utilizada em uma consulta SQL. Retorne **apenas** a pergunta reformulada"
               " sem qualquer texto adicional. "
               "Exemplo: (prompt: Fevereiro, última mensagem no contexto: quais as vendas de janeiro, "
               "então a pergunta reformulada é: quais as vendas de fevereiro). {historico}"),
    ("user", "{texto}"),
])

chain1 = template1 | model | parser
chain2 = template2 | model | parser
chain3 = template3 | model | parser

toolkit = SQLDatabaseToolkit(db=db, llm=model)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

system_message = prompt_template.format(dialect="PyMySQL", top_k=1)

agent_executor = create_react_agent(
    model, toolkit.get_tools(), state_modifier=system_message
)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_logado' in session:
        return redirect(url_for('chatbot'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        resultado = controle.verificar_login(email, senha)
        if resultado:
            usuariologado = resultado
            session['usuario_logado'] = usuariologado

            usuario.idusuario = resultado[0][0]
            usuario.nome = resultado[0][1]
            usuario.email = resultado[0][2]
            usuario.senha = resultado[0][3]

            return redirect(url_for('chatbot'))

    return render_template('login.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        novocadastro = Usuario()

        novocadastro.idusuario = controle.inserir_usuario()
        novocadastro.nome = nome
        novocadastro.email = email
        novocadastro.senha = senha

        alu = novocadastro.inserirDados()
        controle.incluir(alu)
        return render_template('login.html')

    return render_template('cadastro.html')


@app.route('/chatbot')
def chatbot():
    if 'usuario_logado' in session:
        usuariologado = session['usuario_logado']
        quantidadechat = controle.inserir_chat()
        chats = controle.buscar_chats(usuario.idusuario)
        if chats is None:
            chats = []

        return render_template('chatbot.html', usuario=usuariologado, chats=chats,
                               quantidade=quantidadechat, chat_id=0)
    else:
        return render_template('chatvisitante.html')


@app.route('/excluir_chat', methods=['POST'])
def excluir_chat():
    data = request.get_json()
    chat_id = data.get('chatId')

    msgs = Mensagem()
    chatt = Chat()

    msgs.idchat = chat_id
    dmsg = msgs.deletar()
    controle.excluir(dmsg)

    chatt.idchat = chat_id
    chatt.idusuario = usuario.idusuario
    dchat = chatt.deletar()
    controle.excluir(dchat)

    return jsonify({'status': 'success', 'message': 'Chat excluído com sucesso'})


@app.route('/chatbot/<int:chat_id>', methods=['GET', 'POST'])
def chatbotMSG(chat_id):
    checagem = controle.checar_chats(chat_id)
    quantidadechat = controle.inserir_chat()
    if checagem is None or chat_id == 0:
        chat.idchat = quantidadechat
        chat.titulo = 'Nova conversa'
        chat.idusuario = usuario.idusuario
        chat.data = datetime.now().date()

        '''talvez de erro'''
        chat_id = quantidadechat

        newchat = chat.inserirDados()
        controle.incluir(newchat)

    messages = controle.buscar_msg(chat_id)
    if messages is None:
        messages = []

    if 'usuario_logado' in session:
        usuariologado = session['usuario_logado']
        chats = controle.buscar_chats(usuario.idusuario)
        if chats is None:
            chats = []

        return render_template('chatbot.html', usuario=usuariologado, chats=chats, mensagens=messages,
                               quantidade=quantidadechat, chat_id=chat_id)
    else:
        return render_template('chatvisitante.html')


@app.route('/retornar_msgGEMINI', methods=['GET'])
def retornar_msgGEMINI():
    chat_id = request.args.get('chat_id', type=int)
    if not chat_id:
        return jsonify({"error": "chat_id não fornecido"}), 400

    ultimaMsgG = controle.buscar_ultima_msg(chat_id)

    if ultimaMsgG is None:
        return jsonify({"error": "Nenhuma mensagem encontrada para o chat_id fornecido"}), 404

    return jsonify({"ultimaMsgG": ultimaMsgG}), 200


@app.route('/save_message', methods=['POST'])
def save_message():
    data = request.get_json()
    content = data.get('content')
    chat_id = data.get('chatId')
    origin = data.get('origin')
    originbot = data.get('originbot')

    if chat_id == 0:
        quantidadechat = controle.inserir_chat()
        chat.idchat = quantidadechat
        chat.titulo = 'Nova conversa'
        chat.idusuario = usuario.idusuario
        chat.data = datetime.now().date()
        newchat = chat.inserirDados()
        controle.incluir(newchat)
        chat_id = quantidadechat

    try:
        historico = controle.buscar_msg(chat_id)

        mensagem.idmensagem = controle.inserir_mensagem()
        mensagem.conteudo = content
        mensagem.origem = origin
        mensagem.idchat = chat_id
        mensagem.data = datetime.now().date()
        newmsg = mensagem.inserirDados()
        controle.incluir(newmsg)

        texto1 = chain1.invoke({"historico": historico, "texto": content})
        print("chain1: " + texto1)

        if texto1.strip().upper() == "SIM":
            texto3 = chain3.invoke({"historico": historico, "texto": content})
            print("chain3: " + texto3)
            events = agent_executor.invoke({"messages": [("user", texto3)]})
            print(events)

            def extract_text_from_message(message):
                if isinstance(message, AIMessage):
                    if isinstance(message.content, str):
                        return message.content
                    elif isinstance(message.content, list):
                        return ''.join(part.get('text', '') for part in message.content)
                return ""

            last_ai_message = None
            for msg in events.get('messages', []):
                if isinstance(msg, AIMessage):
                    last_ai_message = msg

            if last_ai_message:
                extracted_text = extract_text_from_message(last_ai_message)
                mensagem.conteudo = extracted_text.replace("'", "\\'")
        else:
            texto2 = chain2.invoke({"historico": historico, "texto": content})
            print("chain2: " + texto2)
            mensagem.conteudo = texto2.replace("'", "\\'")

        mensagem.idmensagem = controle.inserir_mensagem()
        mensagem.origem = originbot
        mensagem.idchat = chat_id
        mensagem.data = datetime.now().date()
        newmsg = mensagem.inserirDados()
        controle.incluir(newmsg)

    except Exception as e:
        print(f"Erro no save_message: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success'}), 200


@app.route('/rename_chat', methods=['POST'])
def rename_chat():
    data = request.get_json()
    new_name = data.get('newName')
    chat_id = data.get('chatId')

    if not data or 'newName' not in data or 'chatId' not in data:
        return jsonify({'error': 'Dados inválidos'}), 400

    newNameChat = Chat()
    newNameChat.idchat = chat_id
    newNameChat.titulo = new_name
    newNameChat.idusuario = usuario.idusuario

    newnc = newNameChat.alterar()

    try:
        controle.alterar(newnc)
    except Exception as e:
        print(f"Erro ao alterar o chat: {e}")
        return jsonify({"error": "Failed to update chat"}), 500

    return jsonify({"success": "Chat updated successfully"})


@app.route('/sair', methods=['GET', 'POST'])
def sair():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
