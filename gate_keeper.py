from cgitb import text
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

frame_bottom_left = tk.Frame(frame_bottom)
frame_bottom_left.place(relx=0, rely=0, relwidth=.2, relheight=1)
frame_bottom_left.update()

frame_bottom_right = tk.Frame(frame_bottom)
frame_bottom_right.place(relx=.2, rely=0, relwidth=.8, relheight=1)
frame_bottom_right.update()

frame_bottom_right_left_top = tk.Frame(frame_bottom_right)
frame_bottom_right_left_top.place(relx=0, rely=0, relwidth=.5, relheight=.3)
frame_bottom_right_left_top.update()

frame_bottom_right_left_bottom = tk.Frame(frame_bottom_right)
frame_bottom_right_left_bottom.place(relx=0, rely=.3, relwidth=.5, relheight=.7)
frame_bottom_right_left_bottom.update()

frame_bottom_right_right_top = tk.Frame(frame_bottom_right, bd=5, relief='ridge')
frame_bottom_right_right_top.place(relx=.5, rely=0, relwidth=.5, relheight=.3)
frame_bottom_right_right_top.update()

frame_bottom_right_right_bottom = tk.Frame(frame_bottom_right)
frame_bottom_right_right_bottom.place(relx=.5, rely=.3, relwidth=.5, relheight=.7)
frame_bottom_right_right_bottom.update()

frame_inputs = tk.Frame(frame_bottom_left, bd=5, relief='ridge')
frame_inputs.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_inputs.update()

frame_table = tk.Frame(frame_bottom_right_left_top, bd=5, relief='ridge')
frame_table.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_table.update()

frame_grafico = tk.Frame(janela, bd=5, relief='ridge')
frame_grafico.place(x=0, y=0, relwidth=.5, relheight=.5)
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
input_data.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.1)

button = tk.Button(frame_inputs, text="Dia específico", command=lambda:passage_num_plot(database, canvas, ax, input_data.get_date()))
button.place(relx=0.05, rely=0.2, relwidth=0.45, relheight=0.1)
button = tk.Button(frame_inputs, text="Todos os dias", command=lambda:passage_num_plot(database, canvas, ax, ''))
button.place(relx=0.5, rely=0.2, relwidth=0.45, relheight=0.1)

table = ttk.Treeview(frame_table)
table['columns'] = ("apartamento", "responsavel", "placa")

table.column("#0", width = 0)
table.column("apartamento", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/3))
table.column("responsavel", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/3))
table.column("placa", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/3))

table.heading("apartamento",text="Apartamento", anchor="w")
table.heading("responsavel",text="Responsável", anchor="w")
table.heading("placa",text="Placa", anchor="w")

table.place(relx = 0, rely = 0, relheight=1, relwidth=1)
table_rows = database.get_table_columns()

for id,(apto, apto_info) in enumerate(table_rows.items()):
    if len(apto_info['moradores']) > 1:
        table.insert(parent='', index='end', iid=id, values=(apto, apto_info['responsavel'], apto_info['placa']))
        for id2,morador in enumerate(apto_info['moradores']):
            if morador != apto_info['responsavel']:
                table.insert(parent=id, index='end', iid=f"c{id2}", values=('', morador, ''))
    else:
        table.insert(parent='', index='end', iid=id, values=(apto, apto_info['responsavel'], apto_info['placa']))

apartaments = [0, 1,2,3,4,5,6,7,8,9,10]
apartament_selected = tk.StringVar()
apartament_selected.set(apartaments[0])
apartaments_dropdownbox = ttk.Combobox(frame_bottom_right_left_bottom,
                                         textvariable= apartament_selected,
                                         values=apartaments,
                                         state="readonly")
apartaments_dropdownbox.place(relx=.15,rely=0)
apartaments_dropdownbox.update()

pessoas = database.get_responsaveis()
pessoa_responsavel_selected = tk.StringVar()
pessoa_responsavel_selected.set(list(pessoas.keys())[0])
tipo_pessoa = {"morador":"Morador","responsavel":"Responsável"}
pessoas_dropdownbox = ttk.Combobox(frame_bottom_right_left_bottom,
                                         textvariable= pessoa_responsavel_selected,
                                         values=list(pessoas.keys()),
                                         state="readonly")
pessoas_dropdownbox.place(relx=.55, rely=0)
pessoas_dropdownbox.update()

update_apartament = tk.Button(frame_bottom_right_left_bottom, text="Atualizar apartamento",
                              command=lambda:database.update_apartament(table, apartament_selected.get(),pessoas[pessoa_responsavel_selected.get()]))
update_apartament.place(relx=.35, rely=pessoas_dropdownbox.winfo_height()/frame_bottom_right_left_bottom.winfo_height(),
                        width=pessoas_dropdownbox.winfo_width())
update_apartament.update()

table_pessoas = ttk.Treeview(frame_bottom_right_right_top)
table_pessoas['columns'] = ("nome", "apartamento", "data_nascimento", "status_morador")
table_pessoas['show'] = 'headings'

table_pessoas.column("nome", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()*5/18))
table_pessoas.column("apartamento", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()*1/6))
table_pessoas.column("data_nascimento", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()*5/18))
table_pessoas.column("status_morador", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()*5/18))

table_pessoas.heading("nome",text="Nome", anchor="w")
table_pessoas.heading("apartamento",text="Apto", anchor="w")
table_pessoas.heading("data_nascimento",text="Data de nascimento", anchor="w")
table_pessoas.heading("status_morador",text="Status morador", anchor="w")

table_pessoas.place(relx = 0, rely = 0, relheight=1, relwidth=1)
table_pessoas_rows = database.get_pessoas_columns()

for id,(pessoa, pessoa_info) in enumerate(table_pessoas_rows.items()):   
    table_pessoas.insert(parent='', index='end', iid=id, values=(pessoa, pessoa_info['apartamento'], pessoa_info['data_nascimento'], tipo_pessoa[pessoa_info['tipo_pessoa']]))

nome_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Nome")
nome_pessoa_label.place(relx=0, rely=0, relwidth=0.2, relheight=0.15)
nome_pessoa = tk.Entry(frame_bottom_right_right_bottom)
nome_pessoa.place(relx=.2, rely=0, relwidth=.3, relheight=0.15)

apartament_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Apartamento")
apartament_pessoa_label.place(relx=0, rely=.15, relwidth=0.2, relheight=0.15)
apartament_pessoa_selected = tk.StringVar()
apartament_pessoa_selected.set(apartaments[0])
apartaments_pessoa_dropdownbox = ttk.Combobox(frame_bottom_right_right_bottom,
                                         textvariable= apartament_pessoa_selected,
                                         values=apartaments,
                                         state="readonly")
apartaments_pessoa_dropdownbox.place(relx=.2, rely=.15, relwidth=.3, relheight=0.15)
apartaments_pessoa_dropdownbox.update()

nascimento_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Nascimento")
nascimento_pessoa_label.place(relx=.5, rely=0, relwidth=0.2, relheight=0.15)
nascimento = tkcalendar.DateEntry(frame_bottom_right_right_bottom, state='normal')
nascimento.place(relx=0.7, rely=0, relwidth=.3, relheight=0.15)

tipo_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Status")
tipo_pessoa_label.place(relx=.5, rely=.15, relwidth=0.2, relheight=0.15)

pessoa_selected = tk.StringVar()
pessoa_selected.set(list(tipo_pessoa.values())[0])
tipo_pessoa_dropdownbox = ttk.Combobox(frame_bottom_right_right_bottom,
                                         textvariable= pessoa_selected,
                                         values=list(tipo_pessoa.values()),
                                         state="readonly")
def select_tipo_pessoa(event):
    selected = event.widget.get()
    if selected == "Responsável":
        placa_label.place(relx=.5, rely=.3, relwidth=.2, relheight=0.15)
        placa_entry.place(relx=.7, rely=.3, relwidth=.3, relheight=0.15)
    else:
        placa_label.place_forget()
        placa_entry.place_forget()

placa_label = tk.Label(frame_bottom_right_right_bottom, text="Placa")
placa_entry = tk.Entry(frame_bottom_right_right_bottom)

tipo_pessoa_dropdownbox.bind("<<ComboboxSelected>>",select_tipo_pessoa)
tipo_pessoa_dropdownbox.place(relx=.7, rely=.15, relwidth=.3, relheight=0.15)
tipo_pessoa_dropdownbox.update()

create_pessoa = tk.Button(frame_bottom_right_right_bottom, text="Cadastrar pessoa",
                              command=lambda:database.create_pessoa(table_pessoas,table, (nome_pessoa.get(), apartament_pessoa_selected.get(), nascimento.get_date(), next(chave for chave,valor in tipo_pessoa.items() if valor == pessoa_selected.get()), placa_entry.get()) ))
create_pessoa.place(relx=.25, rely=.6, relwidth=.5, relheight=0.15)
create_pessoa.update()

frame_camera = tk.Frame(janela, bd=5, relief='ridge')
frame_camera.place(relx=.5, rely=0, relwidth=0.5, relheight=0.5)
frame_camera.update()

label = tk.Label(frame_camera, width=frame_camera.winfo_width(), height=frame_camera.winfo_height())
label.place(relx=0, rely=0, relwidth=1, relheight=1)
label.update()

camera = Camera(database, label)
label.after(0, camera.show_frame)

janela.minsize(janela_height, janel_width)
janela.mainloop()
database.close()
