class Chat:

    def __init__(self):
        self.__idchat = ''
        self.__titulo = ''
        '''self.__idmensagem = Mensagem()'''

    @property
    def idchat(self):
        return self.__idchat

    @property
    def titulo(self):
        return self.__titulo


    @idchat.setter
    def idchat(self, entrada):
        self.__idchat = entrada

    @titulo.setter
    def titulo(self, entrada):
        self.__titulo = entrada

    def setChat(self, idchat, titulo):
        self.__idchat = idchat
        self.__titulo = titulo

    def inserirDados(self):
        sql = ("insert into usuario values ('{}','{}')".format(
            self.idchat,
            self.titulo
        ))
        return sql

    def buscar(self):
        sql = "select count(*)+1 from chat"
        return sql