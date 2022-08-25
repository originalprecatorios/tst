# -*- coding: utf-8 -*-
"""
Classe para chamadas simples
"""
import pymysql
from datetime import datetime
from pprint import pprint

class BancoDados:
    def __init__(self, pDatabase):
        vHost = 'localhost'
        vUser = 'root'
        vPass = '123mudar'
        vDb = pDatabase
        self.conn = pymysql.connect(host=vHost, user=vUser, passwd=vPass, db=vDb, charset='utf8', use_unicode=True, cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.conn.close()

    def retorna_query(self, pSQL):
        return self.__returnQuery(pSQL)

    def processa_comando(self, pSQL):
        self.__ExecQuery(pSQL)

    def __returnQuery(self, pSQL):
        #Retorna o resultado da query
        c = self.conn.cursor()
        c.execute(pSQL)
        ret = c.fetchall()
        c.close()
        return ret

    def __returnNow(self):
        #Retorna a data atual no formato de MySQL
        current = datetime.now()
        return "{0}-{1}-{2}".format(current.year, current.month, current.day)

    #Exec updates and inserts
    def __ExecQuery(self, query):
        """
        Executa queryes de insert, update e delete
        """
        if query:
            ex = self.conn.cursor()
            sql = query.replace("'None'", "null")
            ex.execute(sql)
            self.conn.commit()

    def __ajustaCda(self, pValor):
        #formata o CDA para o formato do banco
        if pValor:
            cda = pValor.replace('.', '')
            return "{}".format(cda)

    def __ajustaDataHora(self, pData):
            #Ajusta as data para formato do MySQL
            if pData != '0':
                d = datetime.strptime(pData, '%d/%m/%Y %H:%M:%S').strftime('%Y-%m-%d')
                return "{}".format(d)
            else:
                return 'null'

    def __ajustaDatas(self, pData):
        #Ajusta as data para formato do MySQL
        if pData.strip() != '0':
            d = datetime.strptime(pData.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
            return "{}".format(d)
        else:
            return 'null'

    def __ajustaValor(self, pValor):
        #Trata o valor para o MySQL
        if pValor != '0':
            v = pValor.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            return "{}".format(v)
        else: 
            return "{}".format(pValor)

    def __ajustaTexto(self, pTexto):
        #Trata o texto
        if pTexto:
            #texto = pTexto.encode('ascii', 'ignore').replace("'", "")
            return "'{}'".format(pTexto)

 
    def __ajusta(self, pValor):
        if pValor:
            if type(pValor) == int:
                return pValor
            elif str(type(pValor)) == "<class 'datetime.date'>" or str(type(pValor)) == "<class 'datetime.datetime'>":
                return pValor

            if pValor.find('%') > 0:
                return pValor.replace('%', '').strip()
            if pValor.find('$') > 0 or pValor.find(',') > 2 or pValor.find(',') > 0:
                return self.__ajustaValor(pValor)
            elif pValor.find('/') > 0:
                if len(pValor.split('/')) > 2:
                    if pValor.find(':') > 0:
                        return self.__ajustaDataHora(pValor)
                    elif len(pValor.split('/')) == 3 and len(pValor)<= 11:
                        return self.__ajustaDatas(pValor)
                else:
                    return pValor.replace('.', '').replace('-', '').replace('/', '')

            elif pValor.find('.') > 0:
                if len(pValor.split('.')) == 4:
                    return self.__ajustaCda(pValor)
                else:
                    return pValor.replace("'", "")
            
            return pValor.replace("'", "").strip()
                
    def saveData(self, pDados, pTabela):
        insert = "insert into {}(".format(pTabela)
        values = "values("

        keys = pDados.keys()
        for key in keys:
            insert += "{}, ".format(key)
            values += "'{}', ".format(self.__ajusta(pDados.get(key)))

        insert = insert[0:len(insert)-2] + ")"
        values = values[0:len(values)-2] + ")"
        sql = "{} {} ".format(insert, values)

        print(sql)
        #exit()
        print('inserindo dado:')
        pprint(pDados)
        self.__ExecQuery(sql)
    



    '''
    def saveDadosRN(self, pDados):
        insert = "insert into divida_ativa_rn("
        values = "values("

        keys = pDados.keys()
        for key in keys:
            insert += "{}, ".format(key)
            values += "'{}', ".format(self.__ajusta(pDados.get(key)))

        insert = insert[0:len(insert)-2] + ")"
        values = values[0:len(values)-2] + ")"
        sql = "{} {} ".format(insert, values)

        print(sql)
        #exit()
        print('inserindo dado:')
        pprint(pDados)
        self.__ExecQuery(sql) 
    
    def saveDadosRo(self, pDados):
        insert = "insert into divida_ativa_ro("
        values = "values("

        keys = pDados.keys()
        for key in keys:
            insert += "{}, ".format(key)
            values += "'{}', ".format(self.__ajusta(pDados.get(key)))

        insert = insert[0:len(insert)-2] + ")"
        values = values[0:len(values)-2] + ")"
        sql = "{} {} ".format(insert, values)

        print(sql)
        #exit()
        print('inserindo dado:')
        pprint(pDados)
        self.__ExecQuery(sql)

    def saveDadosSe(self, pDados):
        insert = "insert into divida_ativa_se("
        values = "values("

        keys = pDados.keys()
        for key in keys:
            insert += "{}, ".format(key)
            values += "'{}', ".format(self.__ajusta(pDados.get(key)))

        insert = insert[0:len(insert)-2] + ")"
        values = values[0:len(values)-2] + ")"
        sql = "{} {} ".format(insert, values)

        print(sql)
        #exit()
        print('inserindo dado:')
        pprint(pDados)
        self.__ExecQuery(sql) 

    def saveDadosMs(self, pDados):
        insert = "insert into divida_ativa_ms("
        values = "values("

        keys = pDados.keys()
        for key in keys:
            insert += "{}, ".format(key)
            values += "'{}', ".format(self.__ajusta(pDados.get(key)))

        insert = insert[0:len(insert)-2] + ")"
        values = values[0:len(values)-2] + ")"
        sql = "{} {} ".format(insert, values)

        print(sql)
        #exit()
        print('inserindo dado:')
        pprint(pDados)
        self.__ExecQuery(sql)   
    '''