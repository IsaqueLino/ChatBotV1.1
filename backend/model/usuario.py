from controle import *


class Participante:

    def __init__(self):
        self.__idparticipante = ''
        self.__nome = ''
        self.__prontuario = ''
        self.__cpf = ''
        self.__email = ''
        self.__senha = ''
        self.__nivel_acesso = ''

    @property
    def idparticipante(self):
        return self.__idparticipante

    @property
    def nome(self):
        return self.__nome

    @property
    def prontuario(self):
        return self.__prontuario

    @property
    def cpf(self):
        return self.__cpf

    @property
    def email(self):
        return self.__email

    @property
    def senha(self):
        return self.__senha

    @property
    def nivel_acesso(self):
        return self.__nivel_acesso

    @idparticipante.setter
    def idparticipante(self, entrada):
        self.__idparticipante = entrada

    @nome.setter
    def nome(self, entrada):
        self.__nome = entrada

    @prontuario.setter
    def prontuario(self, entrada):
        self.__prontuario = entrada

    @cpf.setter
    def cpf(self, entrada):
        self.__cpf = entrada

    @email.setter
    def email(self, entrada):
        self.__email = entrada

    @senha.setter
    def senha(self, entrada):
        self.__senha = entrada

    @nivel_acesso.setter
    def nivel_acesso(self, entrada):
        self.__nivel_acesso = entrada

    def setParticipante(self, idparticipante, nome, prontuario, cpf, email, senha, nivel_acesso):
        self.__idparticipante = idparticipante
        self.__nome = nome
        self.__prontuario = prontuario
        self.__cpf = cpf
        self.__email = email
        self.__senha = senha
        self.__nivel_acesso = nivel_acesso

    def inserirDados(self):
        sql = ("insert into participante values ('{}','{}','{}','{}','{}','{}','{}')".format(
            self.idparticipante,
            self.nome,
            self.prontuario,
            self.cpf,
            self.email,
            self.senha,
            self.nivel_acesso,
        ))
        print(sql)
        return sql

    def buscar(self):
        sql = "select count(*)+1 from participante"
        return sql