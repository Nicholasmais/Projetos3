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

    def __format_date__(self, date):
        return datetime.strptime(str(date), "%Y-%m-%d").strftime('%d/%m/%Y')

    def select(self, query):    
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) == 1 and len(rows[0]) == 1:
            return rows[0][0]
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
            pessoas[row[0]] = {'nome':row[1],'cpf':row[2], "apartamento":row[3], "data_nascimento":self.__format_date__(row[4]), "tipo_pessoa":row[5]}
        return pessoas

    def update_apartament(self, apto, responsavel):
        try:
            if self.aptos[int(apto)] != responsavel and self.aptos[int(apto)] != None:
                old_responsavel = self.aptos[int(apto)]
                self.update_pessoa(old_responsavel, self.pessoas_codigo[old_responsavel]['nome'], apto, self.pessoas_codigo[old_responsavel]['data_nascimento'], 'morador')

            if not apto or not responsavel:
                return None
            
            query = 'update apartamento set responsavel = %s where apartamento = %s'
            parameters = (responsavel, apto)
            with self.db.cursor() as cursor:
                cursor.execute(query, parameters)        
                self.db.commit()
            self.update_pessoa(responsavel, self.pessoas_codigo[responsavel]['nome'], self.pessoas_codigo[responsavel]['cpf'], apto, self.pessoas_codigo[responsavel]['data_nascimento'], 'responsavel')                

            return "Sucesso ao atualizar apartamento.", 200
        
        except Exception as e:
            print(e)
            return "Erro ao atuailzar apartamento", 500
        
    def create_pessoa(self, pessoa_dados):
        try:
            query = 'insert into pessoas(nome, cpf, apartamento, data_nascimento, tipo_pessoa) values (%s, %s, %s, %s, %s)'

            val = pessoa_dados

            self.insert(query, val[:-1])
            self.pessoas_codigo = self.get_pessoas()

            query = 'select codigo from pessoas order by codigo desc limit 1;'
            codigo_pessoa_nova = self.select(query)
                    
            if pessoa_dados[4] == 'responsavel':
                query = 'insert into placas_cadastradas(placa, responsavel) values (%s, %s)'
                val = [val[-1], codigo_pessoa_nova]
                self.insert(query, val)
                self.pessoas_placa = self.get_placa_responsavel()

                query = 'select codigo from pessoas order by codigo desc limit 1'
                cursor = self.db.cursor()
                cursor.execute(query)
                res = cursor.fetchall()[0][0]
        
                self.update_apartament(pessoa_dados[2], res)
            return f"Sucesso ao criar {pessoa_dados[3]}", 200
        except Exception as e:
            match e.errno:
                case 1062:
                    return "CPF já cadastrado.", 500
                case 1644:
                    return "Preencha todos os campos", 500
                case _:
                    return f"Erro ao cadastrar {pessoa_dados[3]}", 500

    def get_responsaveis(self):
        query = "SELECT nome,codigo from pessoas where tipo_pessoa = 'responsavel'"        
        responsaveis = {responsavel[0]:responsavel[1] for responsavel in self.select(query)}        
        return responsaveis if responsaveis else {"":""}
    
    def get_pessoas(self):
        query = "SELECT * from pessoas"   
        responsaveis = {responsavel[0]:{
                        "nome":responsavel[1],
                        "cpf":responsavel[2],
                        "apartamento":responsavel[3],
                        "data_nascimento":responsavel[4],
                        "tipo_pessoa":responsavel[5]
                        }
                            for responsavel in self.select(query)}
        return responsaveis

    def get_placa_responsavel(self):
        query = "SELECT responsavel, placa from placas_cadastradas"        
        palcas = {row[0]:row[1] for row in self.select(query)}
        return palcas
    
    def update_pessoa(self, codigo, nome, cpf, apto, data, tipo, placa=None):
        try:
            if placa:
                query = 'update pessoas set nome = %s, cpf = %s, apartamento = %s, data_nascimento = %s, tipo_pessoa = %s where codigo = %s;'
                self.insert(query, [nome, cpf, apto, data, tipo, codigo])
                query = 'update placas_cadastradas set placa = %s where responsavel = %s;'
                self.insert(query, [placa, codigo])
            else:
                query = 'update pessoas set nome = %s, cpf = %s, apartamento = %s, data_nascimento = %s, tipo_pessoa = %s where codigo = %s;'
                self.insert(query, [nome, cpf, apto, data, tipo, codigo])
            return f"Sucesso ao atualizar {tipo}", 200
        except Exception as e:
            print(e)
            return "Erro ao atualizar pessoa", 500
    
    def get_apartamentos(self):
        query = "SELECT * from apartamento"        
        apto = {apto[1]:apto[2] for apto in self.select(query)}
        return apto
    
    def get_logs(self, column = "codigo", order = "desc"):
        query = f"SELECT * from logs order by {column} {order}, codigo"
        logs = {log[0]:{"codigo_veiculo":self.get_responsavel_by_placa_code(log[1]),"data_passagem":self.__format_date__(log[2]),"horario_passagem":log[3],"tipo_passagem":log[4]} for log in self.select(query)}
        return logs
    
    def get_responsavel_by_placa_code(self, placa_code):
        query = f"SELECT placa from placas_cadastradas where codigo = {placa_code}"        
        placa = self.select(query)
        return placa

    def delete_pessoa(self, codigo):
        try:
            query = "delete from pessoas where codigo = %s;"        
            self.insert(query, [codigo])
            return "Sucesso ao deletar", 200
        except Exception as e:
            return "Erro ao deletar", 500