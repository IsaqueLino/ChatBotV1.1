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
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

import secrets
import os

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = secrets.token_urlsafe(32)

controleF = ControleFazenda()
controle = Controle()
usuario = Usuario()
chat = Chat()
mensagem = Mensagem()

load_dotenv()
key_api = os.getenv("CLAUDE_KEY_API")

model2 = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=key_api)
parser = StrOutputParser()

template_unificado = ChatPromptTemplate.from_messages([
    ("system", "Essa informação é sobre protocolos de inseminação para gado de corte ou leite. "
               "Apenas responda perguntas referentes a esse tipo de assunto. "
               "Caso venha algo fora desse contexto, apenas diga que não é capaz de informar sobre aquilo. "
               "Além disso, conversar em ptbr usando esse histórico como contexto e "
               "para continuar a conversa sem a perda de informações "
               "(é para parecer natural sem citar que você recebeu essas informações, "
               "a menos que fale a palavra chave: razen, aí você pode falar sobre o histórico sem problemas): "
               "{protocolo} {historic}"),
    ("user", "{texto}"),
])

chain = template_unificado | model2 | parser



genai.configure(api_key="")

'''model = genai.GenerativeModel('gemini-1.5-flash')'''
model = genai.GenerativeModel('gemini-pro')

chatGemini = model.start_chat(history=[])


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


@app.route('/chatvisitante')
def chatvisitante():
    return render_template('chatvisitante.html')


@app.route('/chatbot')
def chatbot():
    if 'usuario_logado' in session:
        usuariologado = session['usuario_logado']
        quantidadechat = controle.inserir_chat()
        chats = controle.buscar_chats(usuario.idusuario)
        if chats is None:
            chats = []

        return render_template('chatbot.html', usuario=usuariologado, chats=chats, quantidade=quantidadechat, chat_id=0)
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
        protocolos = controleF.buscar_protocolos()
        mensagem.idmensagem = controle.inserir_mensagem()
        mensagem.conteudo = content
        mensagem.origem = origin
        mensagem.idchat = chat_id
        mensagem.data = datetime.now().date()
        newmsg = mensagem.inserirDados()
        controle.incluir(newmsg)

        texto = chain.invoke({"protocolo": protocolos, "historic": historico, "texto": content})
        mensagem.idmensagem = controle.inserir_mensagem()
        mensagem.conteudo = texto
        mensagem.origem = originbot
        mensagem.idchat = chat_id
        mensagem.data = datetime.now().date()
        newmsg = mensagem.inserirDados()
        controle.incluir(newmsg)
    except Exception as e:
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
