import tkinter as tk
from tkinter import ttk
import tkcalendar 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from matplotlib.figure import Figure
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = '0' #webcam externa. Deve vir antes do import cv2

from camera import Camera
from database_handler import DatabaseHandler
from reports import passage_num_plot

database = DatabaseHandler()

janela = tk.Tk()
janela.state("zoomed")
janela.title("GateKeeer")
janela.update()
janela_height = janela.winfo_height()
janel_width = janela.winfo_width()

frame_bottom = tk.Frame(janela, width=int(janel_width*.8), height=janela_height/2)
frame_bottom.place(x=int(janel_width*.1), y=janela_height/2)
frame_bottom.update()

frame_inputs = tk.Frame(frame_bottom, bd=5, relief='ridge')
frame_inputs.place(relx=0, rely=0, relwidth=0.25, relheight=1)
frame_inputs.update()

frame_table = tk.Frame(frame_bottom, bd=5, relief='ridge')
frame_table.place(relx=0.25, rely=0, relwidth=0.75, relheight=1)
frame_table.update()

frame_camera = tk.Frame(janela, bd=5, relief='ridge', width=int(janel_width/2), height=janela_height/2)
frame_camera.place(x=int(janel_width/2), y=0)
frame_camera.update()

label = tk.Label(frame_camera, width=frame_camera.winfo_width(), height=frame_camera.winfo_height())
label.pack()
label.update()

camera = Camera(database, label)
label.after(0, camera.show_frame)

frame_grafico = tk.Frame(janela, bd=5, relief='ridge', width=int(janel_width/2), height=janela_height/2)
frame_grafico.place(x=0, y=0)
frame_grafico.update()

fig = Figure(figsize=((janel_width/2)/100, (janela_height/2)/100), dpi=100)

canvas = FigureCanvasTkAgg(fig,master=frame_grafico)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
canvas._tkcanvas.pack(side='top', fill='both', expand=1)
ax = fig.add_subplot(111)

passage_num_plot(database, canvas, ax, '')

input_data = tkcalendar.DateEntry(frame_inputs, state='normal')
input_data.delete(0, "end")
input_data.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

button = tk.Button(frame_inputs, text="Dia específico", command=lambda:passage_num_plot(database, canvas, ax, input_data.get_date()))
button.place(relx=0.1, rely=0.2, relwidth=0.4, relheight=0.1)
button = tk.Button(frame_inputs, text="Todos os dias", command=lambda:passage_num_plot(database, canvas, ax, ''))
button.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.1)

table = ttk.Treeview(frame_table)
table['columns'] = ("apartamento", "responsavel", "placa")

table.column("#0", width = 0)
table.column("apartamento", anchor="w", stretch=1)
table.column("responsavel", anchor="w", stretch=1)
table.column("placa", anchor="w", stretch=1)

table.heading("apartamento",text="Apartamento", anchor="w")
table.heading("responsavel",text="Responsável", anchor="w")
table.heading("placa",text="Placa", anchor="w")

table.place(relx = 0, rely = .0125, relheight=1, relwidth=1)
table_rows = database.get_table_columns()
print(table_rows)
for id,(apto, apto_info) in enumerate(table_rows.items()):
    if len(apto_info['moradores']) > 1:
        table.insert(parent='', index='end', iid=id, values=(apto, apto_info['responsavel'], apto_info['placa']))
        for id2,morador in enumerate(apto_info['moradores']):
            if morador != apto_info['responsavel']:
                table.insert(parent=id, index='end', iid=f"c{id2}", values=('', morador, ''))
    else:
        table.insert(parent='', index='end', iid=id, values=(apto, apto_info['responsavel'], apto_info['placa']))

janela.minsize(janela_height, janel_width)
janela.mainloop()
database.close()
