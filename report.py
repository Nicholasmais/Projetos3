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

horarios = [f"{hora:02d}h" for hora in range (24)]
bar_width = 0.3

cursor = db.cursor()
query = "select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'entrada' group by hora order by hora"
cursor.execute(query)
row = cursor.fetchall()

data_x_entrada = [int(ponto[0])-bar_width/2 for ponto in row]
data_y_entrada = [int(ponto[1]) for ponto in row]
plt.bar(x=data_x_entrada, height=data_y_entrada, width=bar_width, label="Entrada")

query = "select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'saida' group by hora order by hora"
cursor.execute(query)
row = cursor.fetchall()
db.close()

data_x_saida = [int(ponto[0])+bar_width/2 for ponto in row]
data_y_saida = [int(ponto[1]) for ponto in row]
plt.bar(x=data_x_saida, height=data_y_saida, width=bar_width, label="Saída")

plt.xlabel('Horário')
plt.ylabel('Número de passagens')
plt.title('Passagens por horário')

max_passagens = max(*data_y_entrada, *data_y_saida) + 1
plt.yticks(ticks=[i for i in range(max_passagens)])
plt.xticks(ticks=[hora for hora in range(len(horarios))],
           labels=horarios,
           rotation=360-45)

plt.legend()
plt.show()