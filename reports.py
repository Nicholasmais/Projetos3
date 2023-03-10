from datetime import datetime
import numpy

def absolute_value(val, qtd_passagens):
    a  = numpy.round(val/100.*sum(qtd_passagens), 0)
    if int(a) != 0:
      res = f"{int(a)} morador"
      res += "es" if int(a) > 1 else ''
    else:
      res = ''
    return res
 
def passage_num_plot(database, canvas, ax, dia):
    ax.clear()
    dia = str(dia) if str(dia) != '' else "%" 
    horarios = [f"{hora:02d}h" for hora in range (24)]
    bar_width = 0.3
    
    query = f"select min(data_passagem), max(data_passagem) from logs"    
    data_min, data_max = database.select(query)

    data_min = data_min.strftime('%d/%m/%Y')
    data_max = data_max.strftime('%d/%m/%Y')

    query = f"select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'entrada' and data_passagem like '{dia}' group by hora order by hora"    
    row = database.select(query)

    data_x_entrada = [int(ponto[0])-bar_width/2 for ponto in row]
    data_y_entrada = [int(ponto[1]) for ponto in row]

    query = f"select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'saida' and data_passagem like '{dia}' group by hora order by hora"
    row = database.select(query)

    if len(row) > 0:
        if isinstance(row[0], tuple):
            data_x_saida = [int(ponto[0])+bar_width/2 for ponto in row]
            data_y_saida = [int(ponto[1]) for ponto in row]
        else:
            data_x_saida = [int(ponto[0])+bar_width/2 for ponto in [row]]
            data_y_saida = [int(ponto[1]) for ponto in [row]]
    else:
        data_x_saida = []
        data_y_saida = []

    ax.bar(x=data_x_entrada, height=data_y_entrada, width=bar_width, label="Entrada")
    ax.bar(x=data_x_saida, height=data_y_saida, width=bar_width, label="Saída")

    ax.set_ylabel('Número de passagens')

    dia = f"{data_min} - {data_max}" if dia == "%" else datetime.strptime(dia, "%Y-%m-%d").strftime('%d/%m/%Y')
    ax.set_title(f'Passagens por horário\n{dia}', fontdict={'fontsize':10})

    max_passagens = max([*data_y_entrada, *data_y_saida, 0]) + 1
    ax.set_yticks([i for i in range(max_passagens)])
    ax.set_xticks(ticks=[hora for hora in range(len(horarios))])
    ax.set_xticklabels(labels=horarios, rotation=360-45)

    ax.legend()
    ax.grid(alpha=.25)
    canvas.draw()

def apartament_people_count(database, canvas, ax, plt):
  ax.clear()

  query = 'select apartamento.apartamento, count(pessoas.codigo) from apartamento left join pessoas on apartamento.codigo = pessoas.apartamento group by apartamento;'
  dados = database.select(query)

  apartamentos = [val[0] for val in dados]
  qtd_pessoas = [int(val[1]) for val in dados]

  escala_cores = plt.get_cmap('Blues')
  normalizador = plt.Normalize(min(qtd_pessoas), max(qtd_pessoas))

  ax.bar(apartamentos, qtd_pessoas, color=escala_cores(normalizador(qtd_pessoas)))

  ax.set_title('Número de pessoas por apartamento.')
  ax.set_ylabel("Qtd. Pessoas")
  ax.set_ylim(0, max(qtd_pessoas)+.5)
  ax.set_yticks([tick for tick in range(max(qtd_pessoas)+1)])
  ax.set_xticks(apartamentos)
  ax.grid(alpha=.25)
  canvas.draw()

def pizza(database, canvas, ax, plt):
  ax.clear()

  query = 'SELECT apartamento.apartamento, COUNT(logs.codigo_veiculo) AS count_passagens FROM apartamento LEFT JOIN placas_cadastradas ON apartamento.responsavel = placas_cadastradas.responsavel LEFT JOIN logs ON logs.codigo_veiculo = placas_cadastradas.codigo GROUP BY apartamento.apartamento'
  dados = database.select(query)

  apartamentos = [f"apartamento {row[0]}" for row in dados if row[1] != 0]
  qtd_passagens = [row[1] for row in dados if row[1] != 0]

  escala_cores = plt.get_cmap('YlOrRd')
  normalizador = plt.Normalize(min(qtd_passagens), max(qtd_passagens))

  ax.bar(apartamentos, qtd_passagens, color=escala_cores(normalizador(qtd_passagens)))

  ax.set_title('Número de passagens por apartamento.')
  ax.set_ylabel("Qtd. Passagens")
  ax.set_ylim(0, max(qtd_passagens)+.5)
  ax.set_yticks([tick for tick in range(max(qtd_passagens)+1)])
  ax.set_xticks(apartamentos)
  ax.grid(alpha=.25)

  canvas.draw()

