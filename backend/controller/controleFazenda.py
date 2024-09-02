import re
from backend.dao.persistence import Banco

'''
' OR '1'='1
'''
class Controle:

    def __init__(self):
        self.ob = Banco()
        self.ob.configura(ho="localhost", db="db_chatbot", us="root", se="ifsp")

    def verificar_login(self, email, senha):
        mail = re.sub(r'[^a-zA-Z0-9@._-]', '', email)
        mail = mail.replace("'", "''")

        senha = re.sub(r'[^a-zA-Z0-9@._-]', '', senha)
        senha = senha.replace("'", "''")

        self.ob.abrirConexao()
        sql = f"select * from usuario where email = '{mail}' and senha = '{senha}'"
        resultado = []
        resultado = self.ob.selectQuery(sql)

        if resultado:
            return resultado
        else:
            return None

    def verificar_email(self, email):
        email = re.sub(r'[^a-zA-Z0-9@._-]', '', email)

        email = email.replace("'", "''")
        self.ob.abrirConexao()
        sql = f"select email from usuario where email = '{email}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            email = resultado[0][0]
            return email
        else:
            return None

    def inserir_usuario(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from usuario"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def inserir_chat(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from chat"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def inserir_mensagem(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from mensagem"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def buscar_usuario(self):
        self.ob.abrirConexao()
        sql = f"select * from usuario"
        resultado = []
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_chats(self, idusuario):
        self.ob.abrirConexao()
        sql = f"select * from chat where idusuario= '{idusuario}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            print(resultado)
            return resultado
        else:
            return None

    def checar_chats(self, idchat):
        self.ob.abrirConexao()
        sql = f"select * from chat where idchat= '{idchat}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            print(resultado)
            return resultado
        else:
            return None

    def buscar_msg(self, idchat):
        self.ob.abrirConexao()
        sql = f"select * from mensagem where idchat= '{idchat}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_ultima_msg(self, idchat):
        self.ob.abrirConexao()
        sql = f"select conteudo from mensagem where idchat = '{idchat}' and origem = 1 order by idmensagem desc limit 1"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None
    def incluir(self, info):
        self.ob.abrirConexao()

        sql = info

        try:
            self.ob.execute(sql)
            self.ob.gravar()
        except:
            print("Houve um erro")
            self.ob.descarte()

    def pesquisar(self, info):
        self.ob.abrirConexao()
        dados = self.ob.selectQuery(info)
        dados = dados[0]
        return dados

    def excluir(self, info):
        self.ob.abrirConexao()
        sql = info.excluir()
        try:
            self.ob.execute(sql)
            self.ob.gravar()
        except:
            print("Houve um erro ao excluir o registro")
            self.ob.descarte()

    def alterar(self, info):
        self.ob.abrirConexao()
        sql = info.alterar()
        try:
            self.ob.execute(sql)
            self.ob.gravar()
        except:
            print("Houve um erro ao alterar o registro")
            self.ob.descarte()
