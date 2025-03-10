import re
from backend.dao.persistenceFazenda import BancoFazenda


class ControleFazenda:
    def __init__(self):
        self.ob = BancoFazenda()
        self.ob.configura(ho="localhost", db="fazenda", us="root", se="ifsp")

    def buscar_protocolos(self):
        self.ob.abrirConexao()
        sql = f"select * from protocolos"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_fazendas(self):
        self.ob.abrirConexao()
        sql = f"select * from fazendas"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_bois(self):
        self.ob.abrirConexao()
        sql = f"select * from bois"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_vendedores(self):
        self.ob.abrirConexao()
        sql = f"select * from vendedores"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_inseminadores(self):
        self.ob.abrirConexao()
        sql = f"select * from inseminadores"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_inseminacoes(self):
        self.ob.abrirConexao()
        sql = f"select * from inseminacoes"
        resultado = self.ob.selectQuery(sql)
        if resultado:
            return resultado
        else:
            return None

    def buscar_vendas(self):
        self.ob.abrirConexao()
        sql = f"select * from vendas"
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
