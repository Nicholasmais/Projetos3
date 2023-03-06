import mysql.connector
import configparser
from datetime import datetime

class DatabaseHandler():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('credentials.ini')
        self.db = mysql.connector.connect(
            host=config['credentials']['host'],
            user=config['credentials']["user"],
            password=config['credentials']['password'],
            database=config['credentials']['database']
        )
        self.tipo_pessoa = {"morador":"Morador","responsavel":"Responsável"}
        self.pessoas_codigo = self.get_pessoas()
        self.pessoas_placa = self.get_placa_responsavel()
        self.aptos = self.get_apartamentos()

    def select(self, query):    
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) == 1 and len(rows[0]) != 1:
            return rows[0]
        else:
            return rows

    def insert(self, query, parameters):
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
        self.db.commit()

    def close(self):
        self.db.close()
    
    def get_columns(self, table):        
        query = f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='condominio' AND `TABLE_NAME`='{table}'"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def get_table_columns(self):    
        query = f"select * from pessoas;"
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        pessoas = {}
        for row in res:
            pessoas[row[0]] = row[1]

        query = f"select apartamento.apartamento, pessoas.nome from apartamento left join pessoas on apartamento.codigo = pessoas.apartamento;"
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        pessoas_info = {}

        for row in res:
            if row[0] not in pessoas_info:
                pessoas_info[row[0]] = [row[1]]
            else:
                pessoas_info[row[0]].append(row[1])

        query = f"select apartamento.codigo, apartamento.responsavel, placas_cadastradas.placa from apartamento left join placas_cadastradas on apartamento.responsavel = placas_cadastradas.responsavel order by codigo;"
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        apartaments_info = {}
        for row in res:   
            apartaments_info[row[0]] = {"responsavel":pessoas.get(row[1],""),"moradores":pessoas_info.get(row[0],[]), "placa":row[2] if row[2] else ''}
        return apartaments_info

    def get_pessoas_columns(self):
        query = f"select * from pessoas;"
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        pessoas = {}
        for row in res:
            pessoas[row[1]] = {"apartamento":row[2], "data_nascimento":datetime.strptime(str(row[3]), "%Y-%m-%d").strftime('%d/%m/%Y'), "tipo_pessoa":row[4]}
        return pessoas

    def update_apartament(self, apto, responsavel):
        if self.aptos[int(apto)] != responsavel:
            old_responsavel = self.aptos[int(apto)]
            self.update_pessoa(old_responsavel, self.pessoas_codigo[old_responsavel]['nome'], apto, self.pessoas_codigo[old_responsavel]['data_nascimento'], 'morador')

        if not apto or not responsavel:
            return None
        
        query = 'update apartamento set responsavel = %s where apartamento = %s'
        parameters = (responsavel, apto)
        with self.db.cursor() as cursor:
            cursor.execute(query, parameters)        
            self.db.commit()
        self.update_pessoa(responsavel, self.pessoas_codigo[responsavel]['nome'], apto, self.pessoas_codigo[responsavel]['data_nascimento'], 'responsavel')                

    def create_pessoa(self, pessoa_dados):
        query = 'insert into pessoas(nome, apartamento, data_nascimento, tipo_pessoa) values (%s, %s, %s, %s)'

        val = pessoa_dados
        self.insert(query, val[:-1])
        self.pessoas_codigo = self.get_pessoas()

        query = 'select codigo from pessoas order by codigo desc limit 1;'
        codigo_pessoa_nova = self.select(query)[0][0]
                
        if pessoa_dados[3] == 'responsavel':
          query = 'insert into placas_cadastradas(placa, responsavel) values (%s, %s)'
          val = [val[-1], codigo_pessoa_nova]
          self.insert(query, val)
          self.pessoas_placa = self.get_placa_responsavel()

          query = 'select codigo from pessoas order by codigo desc limit 1'
          cursor = self.db.cursor()
          cursor.execute(query)
          res = cursor.fetchall()[0][0]
  
          self.update_apartament(pessoa_dados[1], res)

    def get_responsaveis(self):
        query = "SELECT nome,codigo from pessoas where tipo_pessoa = 'responsavel'"        
        responsaveis = {responsavel[0]:responsavel[1] for responsavel in self.select(query)}
        return responsaveis
    
    def get_pessoas(self):
        query = "SELECT * from pessoas"        
        responsaveis = {responsavel[0]:{
                        "nome":responsavel[1],
                        "apartamento":responsavel[2],
                        "data_nascimento":responsavel[3],
                        "tipo_pessoa":responsavel[4]
                        }
                            for responsavel in self.select(query)}
        return responsaveis

    def get_placa_responsavel(self):
        query = "SELECT responsavel, placa from placas_cadastradas"        
        palcas = {row[0]:row[1] for row in self.select(query)}
        return palcas
    
    def update_pessoa(self, *pessoa_info):
        query = 'update pessoas set nome = %s, apartamento = %s, data_nascimento = %s, tipo_pessoa = %s where codigo = %s;'
        val = pessoa_info
        self.insert(query, [*val[1:], val[0]])
    
    def get_apartamentos(self):
        query = "SELECT * from apartamento"        
        apto = {apto[1]:apto[2] for apto in self.select(query)}
        return apto