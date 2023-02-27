import matplotlib.pyplot as plt
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('credentials.ini')

db = mysql.connector.connect(
  host=config['credentials']['host'],
  user=config['credentials']["user"],
  password=config['credentials']['password'],
  database=config['credentials']['database']
)
 
cursor = db.cursor()
query = "SELECT * FROM perfil_cadastrados"
cursor.execute(query)
res = cursor.fetchall()
print(res)
