import mysql.connector
import configparser

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

        query = f"select apartamento.apartamento, pessoas.nome from apartamento inner join pessoas on apartamento.codigo = pessoas.apartamento;"
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        pessoas_info = {}

        for row in res:
            if row[0] not in pessoas_info:
                pessoas_info[row[0]] = [row[1]]
            else:
                pessoas_info[row[0]].append(row[1])

        query = f"select apartamento.*, placas_cadastradas.placa from apartamento inner join placas_cadastradas on apartamento.responsavel = placas_cadastradas.responsavel;"
        cursor = self.db.cursor()
        cursor.execute(query)
        res = cursor.fetchall()
        apartaments_info = {}
        for row in res:   
            apartaments_info[row[1]] = {"responsavel":pessoas[row[2]],"moradores":pessoas_info[row[1]], "placa":row[3]}
        return apartaments_info
    #apartemtno responsavel placa