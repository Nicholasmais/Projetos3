from datetime import datetime

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
    
    if isinstance(row[0], tuple):
        data_x_saida = [int(ponto[0])+bar_width/2 for ponto in row]
        data_y_saida = [int(ponto[1]) for ponto in row]
    else:
        data_x_saida = [int(ponto[0])+bar_width/2 for ponto in [row]]
        data_y_saida = [int(ponto[1]) for ponto in [row]]
        
    ax.bar(x=data_x_entrada, height=data_y_entrada, width=bar_width, label="Entrada")
    ax.bar(x=data_x_saida, height=data_y_saida, width=bar_width, label="Saída")

    ax.set_xlabel('Horário')
    ax.set_ylabel('Número de passagens')

    dia = f"{data_min} - {data_max}" if dia == "%" else datetime.strptime(dia, "%Y-%m-%d").strftime('%d/%m/%Y')
    ax.set_title(f'Passagens por horário\n{dia}', fontdict={'fontsize':10})

    max_passagens = max([*data_y_entrada, *data_y_saida, 0]) + 1
    ax.set_yticks(ticks=[i for i in range(max_passagens)])
    ax.set_xticks(ticks=[hora for hora in range(len(horarios))])
    ax.set_xticklabels(labels=horarios, rotation=360-45)

    ax.legend()
    ax.grid(alpha=.25)
    canvas.draw()