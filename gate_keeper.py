import tkinter as tk
import tkcalendar 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import configparser
from datetime import datetime
from matplotlib.figure import Figure
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = '0' #webcam externa. Deve vir antes do import cv2

import cv2
import pytesseract
from PIL import Image, ImageTk

import random
import time

config = configparser.ConfigParser()
config.read('credentials.ini')

db = mysql.connector.connect(
host=config['credentials']['host'],
user=config['credentials']["user"],
password=config['credentials']['password'],
database=config['credentials']['database']
)

cursor = db.cursor()
query = "SELECT * FROM placas_cadastradas"
cursor.execute(query)
res = cursor.fetchall()

placas_cadastradas = {placa:{'nome':responsavel, 'codigo':codigo} for codigo, placa, responsavel in res}
passagem_dict = {0:"entrada",1:"saida"}

#https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
capture = cv2.VideoCapture(0)

min_width, max_width = 80, 250
plate_ratio = 150/60

janela = tk.Tk()
janela.state("zoomed")
janela.title("GateKeeer")
janela.update()

janela_height = janela.winfo_height()
janel_width = janela.winfo_width()

def update_plot(dia):

    ax.clear()
    dia = str(dia) if str(dia) != '' else "%" 
    horarios = [f"{hora:02d}h" for hora in range (24)]
    bar_width = 0.3

    cursor = db.cursor()
    query = f"select min(data_passagem), max(data_passagem) from logs"
    cursor.execute(query)
    data_min, data_max = cursor.fetchall()[0]
    data_min = data_min.strftime('%d/%m/%Y')
    data_max = data_max.strftime('%d/%m/%Y')

    cursor = db.cursor()
    query = f"select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'entrada' and data_passagem like '{dia}' group by hora order by hora"
    cursor.execute(query)
    row = cursor.fetchall()

    data_x_entrada = [int(ponto[0])-bar_width/2 for ponto in row]
    data_y_entrada = [int(ponto[1]) for ponto in row]

    query = f"select date_format(horario_passagem, '%H') as hora, count(passagem) from logs where passagem = 'saida' and data_passagem like '{dia}' group by hora order by hora"
    cursor.execute(query)
    row = cursor.fetchall()

    data_x_saida = [int(ponto[0])+bar_width/2 for ponto in row]
    data_y_saida = [int(ponto[1]) for ponto in row]

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

frame_inputs = tk.Frame(janela, bd=5, relief='ridge', width=int(janel_width*.8), height=janela_height/2)
frame_inputs.place(x=int(janel_width*.1), y=janela_height/2)

frame_camera = tk.Frame(janela, bd=5, relief='ridge', width=int(janel_width/2), height=janela_height/2)
frame_camera.place(x=int(janel_width/2), y=0)
frame_camera.update()

label = tk.Label(frame_camera, width=frame_camera.winfo_width(), height=frame_camera.winfo_height())
label.pack()
label.update()

capture = cv2.VideoCapture(0)
def show_frame():
    ret, frame = capture.read()
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray_frame, 50, 150)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # filtrar contornos para encontrar apenas retângulos
    rectangles = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h        
            if (min_width < w and w < max_width) and (plate_ratio*.9 < aspect_ratio < plate_ratio*1.1):  # adiciona apenas retângulos que são menores que os tamanhos máximos especificados
                rectangles.append(approx)
    
    cores = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in rectangles]
    
    color_gray_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)#para os retangulo coloridos na imagem cinza
    # desenhar retângulos na imagem
    for i, rectangle in enumerate(rectangles):
        
        # obter as coordenadas do retângulo
        x, y, w, h = cv2.boundingRect(rectangle)
        cor = cores[i]
        cv2.rectangle(color_gray_frame, (x, y), (x + w, y + h), cor, 2)
        
        # Insere o texto correspondente a cada retângulo
        texto = f"Retangulo {i+1} width = {w} height = {h}"
        cv2.putText(color_gray_frame, texto, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

        cropped_image = color_gray_frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cropped_image).strip()
        #Exibe o texto associado ao retângulo
        cv2.putText(color_gray_frame, text, (x, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

        if text in placas_cadastradas:     
            t = time.localtime()
            data_passagem = time.strftime("%Y-%m-%d", t)
            horario_passagem = time.strftime("%H:%M:%S", t)
            passagem = int(horario_passagem[-2:]) % 2

            entrada = f"{placas_cadastradas[text]['nome']} permitida a {passagem_dict[passagem]}."
            cv2.putText(color_gray_frame, entrada, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 1)
            
            sql = "insert into logs(codigo_veiculo, data_passagem, horario_passagem, passagem) values(%s,%s,%s,%s)"
            val = (int(placas_cadastradas[text]['codigo']),data_passagem, horario_passagem, passagem_dict[passagem])
            cursor.execute(sql, val)
            db.commit()

            for tempo in (range(3,0,-1)):
                cv2.rectangle(color_gray_frame, (0, 0), (100, 40), (0,0,0), -1)
                cv2.putText(color_gray_frame, f"Aguarde {tempo}s", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 1)
                #cv2.imshow("Camera2", color_gray_frame)          
                cv2.waitKey(1000)
    
    if ret:
        cv2.resize(color_gray_frame, (label.winfo_width(), label.winfo_height()))
        image = Image.fromarray(color_gray_frame)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
    # Chama esta função novamente em 30 milissegundos
    label.after(30, show_frame)
    
label.after(0, show_frame)

frame_grafico = tk.Frame(janela, bd=5, relief='ridge', width=int(janel_width/2), height=janela_height/2)
frame_grafico.place(x=0, y=0)
frame_grafico.update()

fig = Figure(figsize=((janel_width/2)/100, (janela_height/2)/100), dpi=100)

canvas = FigureCanvasTkAgg(fig,master=frame_grafico)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
canvas._tkcanvas.pack(side='top', fill='both', expand=1)
ax = fig.add_subplot(111)
update_plot('')
input_data = tkcalendar.DateEntry(frame_inputs, state='normal')
input_data.delete(0, "end")
input_data.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)

button = tk.Button(frame_inputs, text="Dia específico", command=lambda:update_plot(input_data.get_date()))
button.place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.1)
button = tk.Button(frame_inputs, text="Todos os dias", command=lambda:update_plot(''))
button.place(relx=0.2, rely=0.2, relwidth=0.1, relheight=0.1)

janela.minsize(janela_height, janel_width)
janela.mainloop()
db.close()
