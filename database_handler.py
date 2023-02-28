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
    