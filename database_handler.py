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
        return None

    def close(self):
        self.db.close()
        return None
    
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
        query = 'update apartamento set responsavel = %s where apartamento = %s'
        parameters = (responsavel, apto)
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
   
        self.db.commit()
        print("Apartamento atualizado")

    def create_pessoa(self, tkinter_table, pessoa_dados):
        query = 'insert into pessoas(nome, apartamento, data_nascimento, tipo_pessoa) values (%s, %s, %s, %s)'
        val = pessoa_dados
        
        self.insert(query, val)
        
        tkinter_table.insert(parent='', index='end', iid=id, values=(pessoa_dados[0], pessoa_dados[1], pessoa_dados[2], self.tipo_pessoa[pessoa_dados[3]]))

        if pessoa_dados[3] == 'morador':
          query = 'select codigo from pessoas order by codigo desc limit 1'
          cursor = self.db.cursor()
          cursor.execute(query)
          res = cursor.fetchall()[0][0]
          self.update_apartament(pessoa_dados[1], res)
        return None