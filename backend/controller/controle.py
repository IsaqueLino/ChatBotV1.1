from conectarbanco import *
import re

'''
' OR '1'='1
'''
class Controle:

    def __init__(self):
        self.ob = Banco()
        self.ob.configura(ho="localhost", db="db_evento", us="root", se="ifsp")

    def verificar_login(self, prontuario, senha):
        prontuario = re.sub(r'[^a-zA-Z0-9@._-]', '', prontuario)
        prontuario = prontuario.replace("'", "''")

        senha = re.sub(r'[^a-zA-Z0-9@._-]', '', senha)
        senha = senha.replace("'", "''")

        self.ob.abrirConexao()
        sql = f"select * from participante where prontuario = '{prontuario}' and senha = '{senha}'"
        resultado = []
        resultado = self.ob.selectQuery(sql)

        if resultado:
            return resultado
        else:
            sql = f"select * from participante where cpf = '{prontuario}' and senha = '{senha}'"
            resultado = self.ob.selectQuery(sql)

            if resultado:
                return resultado
            else:
                return None
    def verifica_nivel(self, prontuario):
        prontuario = re.sub(r'[^a-zA-Z0-9@._-]', '', prontuario)

        prontuario = prontuario.replace("'", "''")
        self.ob.abrirConexao()
        sql = f"select nivel_acesso from participante where prontuario = '{prontuario}'"
        resultado = self.ob.selectQuery(sql)

        if resultado:
            nivel_usuario = resultado[0][0]
            return nivel_usuario
        else:
            sql = f"select nivel_acesso from participante where cpf = '{prontuario}'"
            resultado = self.ob.selectQuery(sql)

            if resultado:
                nivel_usuario = resultado[0][0]
                return nivel_usuario
            else:
                return None

    def verificar_email(self, email):
        email = re.sub(r'[^a-zA-Z0-9@._-]', '', email)

        email = email.replace("'", "''")
        self.ob.abrirConexao()
        sql = f"select email from participante where email = '{email}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            email = resultado[0][0]
            return email
        else:
            return None

    def inserir_participante(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from participante"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def inserir_semana(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from semana"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def inserir_palestrante(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from palestrante"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def inserir_evento(self):
        self.ob.abrirConexao()
        sql = f"select count(*)+1 from evento"
        resultado = self.ob.selectQuery(sql)
        quantidade = resultado[0][0]
        if resultado:
            return quantidade
        else:
            return None

    def buscar_palestrantes(self):
        self.ob.abrirConexao()
        sql = f"select * from palestrante"
        resultado = []
        resultado = self.ob.selectQuery(sql)
        if resultado:
            palestrantes = resultado
            return palestrantes
        else:
            return None

    def buscar_eventos(self):
        self.ob.abrirConexao()
        sql = f"select * from evento"
        resultado = []
        resultado = self.ob.selectQuery(sql)
        if resultado:
            eventos = resultado
            return eventos
        else:
            return None

    def buscar_semanas(self):
        self.ob.abrirConexao()
        sql = f"select * from semana"
        resultado = []
        resultado = self.ob.selectQuery(sql)
        if resultado:
            semanas = resultado
            return semanas
        else:
            return None

    def buscar_idsemana(self, semana):
        self.ob.abrirConexao()
        sql = f"select idsemana from semana where idsemana= '{semana[0]}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            idsemana = resultado
            return idsemana
        else:
            return None

    def buscar_semana(self, semana):
        self.ob.abrirConexao()
        sql = f"select * from semana where idsemana= '{semana[0]}'"
        resultado = []
        resultado = self.ob.selectQuery(sql)
        if resultado:
            idsemana = resultado
            return idsemana
        else:
            return None

    def buscar_idpalestrante(self, palestrante):
        self.ob.abrirConexao()
        sql = f"select idpalestrante from palestrante where idpalestrante= '{palestrante[0]}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            idpalestrante = resultado
            return idpalestrante
        else:
            return None

    def buscar_participantes(self):
        self.ob.abrirConexao()
        sql = f"select * from participante"
        resultado = []
        resultado = self.ob.selectQuery(sql)
        if resultado:
            semanas = resultado
            return semanas
        else:
            return None

    def buscar_ideventos(self, semana):
        self.ob.abrirConexao()
        sql = f"select * from evento where idsemana= '{semana[0]}'"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            res = resultado
            return res
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

    def procuraRegistro(self, info):
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
