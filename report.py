import matplotlib.pyplot as plt
import mysql.connector
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read('credentials.ini')

db = mysql.connector.connect(
  host=config['credentials']['host'],
  user=config['credentials']["user"],
  password=config['credentials']['password'],
  database=config['credentials']['database']
)

horarios = [f"{hora:02d}h" for hora in range (24)]
bar_width = 0.3

cursor = db.cursor()
query = f"select min(data_passagem), max(data_passagem) from logs"
cursor.execute(query)
data_min, data_max = cursor.fetchall()[0]
data_min = data_min.strftime('%d/%m/%Y')
data_max = data_max.strftime('%d/%m/%Y')

dia = False
data = dia if dia else "%"

cursor = db.cursor()
query = f"select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'entrada' and data_passagem like '{data}' group by hora order by hora"
cursor.execute(query)
row = cursor.fetchall()

data_x_entrada = [int(ponto[0])-bar_width/2 for ponto in row]
data_y_entrada = [int(ponto[1]) for ponto in row]
plt.bar(x=data_x_entrada, height=data_y_entrada, width=bar_width, label="Entrada")

query = f"select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'saida' and data_passagem like '{data}' group by hora order by hora"
cursor.execute(query)
row = cursor.fetchall()
db.close()

data_x_saida = [int(ponto[0])+bar_width/2 for ponto in row]
data_y_saida = [int(ponto[1]) for ponto in row]
plt.bar(x=data_x_saida, height=data_y_saida, width=bar_width, label="Saída")

plt.xlabel('Horário')
plt.ylabel('Número de passagens')
plt.title('Passagens por horário')

max_passagens = max([*data_y_entrada, *data_y_saida, 0]) + 1
plt.yticks(ticks=[i for i in range(max_passagens)])
plt.xticks(ticks=[hora for hora in range(len(horarios))],
           labels=horarios,
           rotation=360-45)

data = f"{data_min} - {data_max}" if data == "%" else datetime.strptime(data, "%Y-%m-%d").strftime('%d/%m/%Y')
plt.text(0.25, max_passagens - 1, data, fontsize=10)

plt.legend()
plt.grid(alpha=.25)
plt.show()