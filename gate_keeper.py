import tkinter as tk
from tkinter import ttk
from click import command
import tkcalendar 

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = '0' #webcam externa. Deve vir antes do import cv2

from camera import Camera
from database_handler import DatabaseHandler
from reports import passage_num_plot, apartament_people_count, pizza

database = DatabaseHandler()

janela = tk.Tk()
janela.state("zoomed")
janela.title("GateKeeer")
janela.config(bg='lightblue')
janela.update()
janela_height = janela.winfo_height()
janel_width = janela.winfo_width()

style=ttk.Style()
style.theme_use('alt')
style.configure("Vertical.TScrollbar", background="lightblue")
style.configure('TCombobox', foreground='black', 
                background='lightblue',
                arrowcolor='darkblue',
                fieldbackground='white')
style.map('TCombobox', fieldbackground=[('readonly', 'white')])
style.configure('TCombobox.entry', background='lightblue')
style.configure('TButton', foreground='black', background='lightblue')
style.map('TButton', background=[('active', '#E0FFFF')])
style.configure('TRadiobutton', foreground='black', background='lightblue', jusitfy="center")
style.map('TRadiobutton', background=[('active', '#E0FFFF')])

frame_bottom = tk.Frame(janela, bd=5, relief='ridge',bg='#F7DC6F')
frame_bottom.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.5)
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

frame_bottom_right_right_top = tk.Frame(frame_bottom_right, bd=5, relief='ridge', bg='#F7DC6F')
frame_bottom_right_right_top.place(relx=.5, rely=0, relwidth=.5, relheight=.3)
frame_bottom_right_right_top.update()

frame_bottom_right_right_bottom = tk.Frame(frame_bottom_right)
frame_bottom_right_right_bottom.place(relx=.5, rely=.3, relwidth=.5, relheight=.7)
frame_bottom_right_right_bottom.update()

frame_input_border_color = tk.Frame(frame_bottom_left, bd=5, relief='ridge', bg='#F7DC6F')
frame_input_border_color.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_inputs = tk.Frame(frame_input_border_color)
frame_inputs.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_inputs.update()

frame_table = tk.Frame(frame_bottom_right_left_top, bd=5, relief='ridge',bg='#F7DC6F')
frame_table.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_table.update()

frame_grafico = tk.Frame(janela, bd=5, relief='ridge',bg='#F7DC6F')
frame_grafico.place(x=0, y=0, relwidth=.5, relheight=.5)
frame_grafico.update()

fig = Figure(figsize=((janel_width/2)/100, (janela_height/2)/100), dpi=100)

canvas = FigureCanvasTkAgg(fig,master=frame_grafico)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
canvas._tkcanvas.pack(side='top', fill='both', expand=1)
ax = fig.add_subplot(111)

passage_num_plot(database, canvas, ax, '')

input_data = tkcalendar.DateEntry(frame_inputs, state='normal', date_pattern='dd/MM/yyyy')
input_data.delete(0, "end")
input_data.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.1)

def change_graph(dia):
    option = graph_selected.get()
    match option:
        case "num_pass":
          fig.set_size_inches((janel_width/2.03125)/100, (janela_height/2.06)/100)
          passage_num_plot(database, canvas, ax, dia)
        case "apto_count":
          fig.set_size_inches((janel_width/2)/100, (janela_height/2)/100)
          apartament_people_count(database, canvas, ax, plt, dia)
        case "pizza":
          fig.set_size_inches((janel_width/2)/100, (janela_height/2)/100)          
          pizza(database, canvas, ax, dia)

button = ttk.Button(frame_inputs, text="Dia específico", command=lambda :change_graph(input_data.get()))
button.place(relx=0.05, rely=0.2, relwidth=0.45, relheight=0.1)
button = ttk.Button(frame_inputs, text="Todos os dias", command=lambda :change_graph(''))
button.place(relx=0.5, rely=0.2, relwidth=0.45, relheight=0.1)

grafico_label_text = tk.Label(frame_inputs, text="Selecionar gráfico")
grafico_label_text.place(relx = 0, rely = 0.3, relwidth = 1, relheight = 0.1)

graph_selected = tk.StringVar()
graph_selected.set("num_pass")

graph_option1 = ttk.Radiobutton(frame_inputs, text = "Passagens por horário", value = "num_pass", variable = graph_selected, command=lambda: change_graph(''), takefocus=False)
graph_option2 = ttk.Radiobutton(frame_inputs, text = "Pessoas por apartamento", value = "apto_count", variable = graph_selected, command=lambda: change_graph(''), takefocus=False)
graph_option3 = ttk.Radiobutton(frame_inputs, text = "Passagens por apartamento", value = "pizza", variable = graph_selected, command=lambda: change_graph(''), takefocus=False)

graph_option1.place(relx = 0.05, rely = 0.4, relwidth = 0.9, relheight = 0.1)
graph_option2.place(relx = 0.05, rely = 0.5, relwidth = 0.9, relheight = 0.1)
graph_option3.place(relx = 0.05, rely = 0.6, relwidth = 0.9, relheight = 0.1)

def set_scrollbar_table(table, frame, last_table = 0):    
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=table.yview)
    if last_table:
        scrollbar.place(relx=1.0, rely=.79, relheight=.2125, anchor='ne')
    else:
        scrollbar.place(relx=1.0, rely=0, relheight=1.0, anchor='ne')
    table.configure(yscrollcommand=scrollbar.set)

table = ttk.Treeview(frame_table)
set_scrollbar_table(table, frame_table)
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
                table.insert(parent=id, index='end', iid=f"M-{id}-{id2}", values=('', morador, ''))
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

table_pessoas = ttk.Treeview(frame_bottom_right_right_top)
set_scrollbar_table(table_pessoas, frame_bottom_right_right_top)
table_pessoas['columns'] = ("nome", "cpf", "data_nascimento", "apartamento", "status_morador")
table_pessoas['show'] = 'headings'

table_pessoas.column("nome", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/5))
table_pessoas.column("cpf", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/5))
table_pessoas.column("data_nascimento", anchor="w", stretch=0, width = int(2.5*frame_bottom_right_left_top.winfo_width()/10))
table_pessoas.column("apartamento", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/10))
table_pessoas.column("status_morador", anchor="w", stretch=0, width = int(frame_bottom_right_left_top.winfo_width()/5))

table_pessoas.heading("nome",text="Nome", anchor="w")
table_pessoas.heading("cpf",text="CPF", anchor="w")
table_pessoas.heading("data_nascimento",text="Data de nascimento", anchor="w")
table_pessoas.heading("apartamento",text="Apto", anchor="w")
table_pessoas.heading("status_morador",text="Status morador", anchor="w")

table_pessoas.place(relx = 0, rely = 0, relheight=1, relwidth=1)
table_pessoas_rows = database.get_pessoas_columns()

tipo_pessoa = {"morador":"Morador","responsavel":"Responsável"}

for codigo, pessoa_info in table_pessoas_rows.items():
    table_pessoas.insert(parent='', index='end', iid=codigo, values=(pessoa_info['nome'], pessoa_info['cpf'], pessoa_info['data_nascimento'], pessoa_info['apartamento'], tipo_pessoa[pessoa_info['tipo_pessoa']]))

pessoas = database.get_responsaveis()
pessoa_responsavel_selected = tk.StringVar()
pessoa_responsavel_selected.set(list(pessoas.keys())[0])
pessoas_dropdownbox = ttk.Combobox(frame_bottom_right_left_bottom,
                                         textvariable= pessoa_responsavel_selected,
                                         values=list(pessoas.keys()),
                                         state="readonly")
pessoas_dropdownbox.place(relx=.55, rely=0)
pessoas_dropdownbox.update()

table_logs = ttk.Treeview(frame_bottom_right)
set_scrollbar_table(table_logs, frame_bottom_right, 1)
table_logs['columns'] = ("codigo", "codigo_veiculo", "data_passagem","horario_passagem", "passagem")
table_logs['show'] = 'headings'

table_logs.column("codigo", anchor="w", stretch=0, width = int(frame_bottom_right.winfo_width()/5))
table_logs.column("codigo_veiculo", anchor="w", stretch=0, width = int(frame_bottom_right.winfo_width()/5))
table_logs.column("data_passagem", anchor="w", stretch=0, width = int(frame_bottom_right.winfo_width()/5))
table_logs.column("horario_passagem", anchor="w", stretch=0, width = int(frame_bottom_right.winfo_width()/5))
table_logs.column("passagem", anchor="w", stretch=0, width = int(frame_bottom_right.winfo_width()/5))

order = "desc"
def sort_logs(column):
    global order
    table_logs.delete(*table_logs.get_children())    
    table_logs_rows = database.get_logs(column, order)
    order = "asc" if order == "desc" else "desc"
    for id,(codigo, log_info) in enumerate(table_logs_rows.items()):
        table_logs.insert(parent='', index='end', iid=id, values=(codigo,
                                                                log_info['codigo_veiculo'],
                                                                log_info['data_passagem'],
                                                                log_info['horario_passagem'],
                                                                tipo_passagem[log_info['tipo_passagem']])
                                                                )

from PIL import Image, ImageTk
with Image.open("arrows.png") as img:
    img_resized = img.resize((16, 16), resample=Image.BILINEAR)
    sorting_arrows = ImageTk.PhotoImage(img_resized)

table_logs.heading("codigo",text="Código", anchor="w", image=sorting_arrows, command=lambda :sort_logs("codigo"))
table_logs.heading("codigo_veiculo",text="Placa Veículo", anchor="w", image=sorting_arrows, command=lambda :sort_logs("codigo_veiculo"))
table_logs.heading("data_passagem",text="Data da passagem", anchor="w", image=sorting_arrows, command=lambda :sort_logs("data_passagem"))
table_logs.heading("horario_passagem",text="Horário da passagem", anchor="w", image=sorting_arrows, command=lambda :sort_logs("horario_passagem"))
table_logs.heading("passagem",text="Tipo de passagem", anchor="w", image=sorting_arrows, command=lambda :sort_logs("passagem"))

table_logs.place(relx = 0, rely = .725, relheight=.275, relwidth=1)
table_logs_rows = database.get_logs()
tipo_passagem = {"entrada":"Entrada","saida":"Saída"}

for id,(codigo, log_info) in enumerate(table_logs_rows.items()):
    table_logs.insert(parent='', index='end', iid=id, 
                       values=(codigo,
                            log_info['codigo_veiculo'],
                            log_info['data_passagem'],
                            log_info['horario_passagem'],
                            tipo_passagem[log_info['tipo_passagem']])
                            )

def refresh_tables():
    try:
        #Tabela apartamentos
        table.delete(*table.get_children())
        table_rows = database.get_table_columns()    
        for id,(apto, apto_info) in enumerate(table_rows.items()):
            if len(apto_info['moradores']) > 1:
                table.insert(parent='', index='end', iid=id, values=(apto, apto_info['responsavel'], apto_info['placa']))
                for id2,morador in enumerate(apto_info['moradores']):
                    if morador != apto_info['responsavel']:
                        table.insert(parent=id, index='end', iid=f"M-{id}-{id2}", values=('', morador, ''))
            else:
                table.insert(parent='', index='end', iid=id, values=(apto, apto_info['responsavel'], apto_info['placa']))
        pessoas_dropdownbox_new = database.get_responsaveis()
        pessoas_dropdownbox['values'] = list(pessoas_dropdownbox_new.keys())

        #Tabela pessoas
        table_pessoas.delete(*table_pessoas.get_children())
        table_pessoas_rows = database.get_pessoas_columns()
        for codigo, pessoa_info in table_pessoas_rows.items():
            table_pessoas.insert(parent='', index='end', iid=codigo, values=(pessoa_info['nome'], pessoa_info['cpf'], pessoa_info['data_nascimento'], pessoa_info['apartamento'], tipo_pessoa[pessoa_info['tipo_pessoa']]))
        
        #Tabela logs
        table_logs.delete(*table_logs.get_children())
        table_logs_rows = database.get_logs()
        for id,(codigo, log_info) in enumerate(table_logs_rows.items()):   
            table_logs.insert(parent='', index='end', iid=id, values=(codigo,
                                                                log_info['codigo_veiculo'],
                                                                log_info['data_passagem'],
                                                                log_info['horario_passagem'],
                                                                tipo_passagem[log_info['tipo_passagem']])
                                                                )
        
        #camera
        update_camera()

        #graficos
        change_graph(input_data.get())
    except Exception as e:
        print(e)
        show_popup("Erro ao atualizar tabelas", 400)

def update_apartament():
    mes, status = database.update_apartament(apartament_selected.get(),pessoas[pessoa_responsavel_selected.get()])
    show_popup(mes,status)
    refresh_tables()

def show_popup(mensagem, status):
    popup = ttk.Label(frame_bottom, text=mensagem, anchor="center")
    match status:
        case 200:
            popup.configure(background="green")
        case 400:
            popup.configure(background="yellow")
        case 500:
            popup.configure(background='red')
    popup.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.2)
    popup.after(3000, popup.destroy)

update_apartament_button = ttk.Button(frame_bottom_right_left_bottom, text="Atualizar apartamento",
                              command=update_apartament)
update_apartament_button.place(relx=.35, rely=pessoas_dropdownbox.winfo_height()/frame_bottom_right_left_bottom.winfo_height(),
                        width=pessoas_dropdownbox.winfo_width())
update_apartament_button.update()

nome_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Nome")
nome_pessoa_label.place(relx=0, rely=0, relwidth=0.2, relheight=0.1)
nome_pessoa = tk.Entry(frame_bottom_right_right_bottom)
nome_pessoa.place(relx=.2, rely=0, relwidth=.3, relheight=0.1)

apartament_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Apartamento")
apartament_pessoa_label.place(relx=.5, rely=0, relwidth=0.2, relheight=0.1)
apartament_pessoa_selected = tk.StringVar()
apartament_pessoa_selected.set(apartaments[0])
apartaments_pessoa_dropdownbox = ttk.Combobox(frame_bottom_right_right_bottom,
                                         textvariable= apartament_pessoa_selected,
                                         values=apartaments,
                                         state="readonly")
apartaments_pessoa_dropdownbox.place(relx=0.7, rely=0, relwidth=.3, relheight=0.1)
apartaments_pessoa_dropdownbox.update()

nascimento_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Nascimento")
nascimento_pessoa_label.place(relx=0, rely=.1, relwidth=0.2, relheight=0.1)
nascimento = tkcalendar.DateEntry(frame_bottom_right_right_bottom, state='normal', date_pattern='dd/MM/yyyy')
nascimento.place(relx=.2, rely=.1, relwidth=.3, relheight=0.1)

cpf_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="CPF")
cpf_pessoa_label.place(relx=0, rely=.2, relwidth=0.2, relheight=0.1)
cpf = tk.Entry(frame_bottom_right_right_bottom)
cpf.place(relx=.2, rely=.2, relwidth=.3, relheight=0.1)

tipo_pessoa_label = tk.Label(frame_bottom_right_right_bottom, text="Status")
tipo_pessoa_label.place(relx=.5, rely=.1, relwidth=0.2, relheight=0.1)

pessoa_selected = tk.StringVar()
pessoa_selected.set(list(tipo_pessoa.values())[0])
tipo_pessoa_dropdownbox = ttk.Combobox(frame_bottom_right_right_bottom,
                                         textvariable= pessoa_selected,
                                         values=list(tipo_pessoa.values()),
                                         state="readonly")

def select_tipo_pessoa(event, tipo_pessoa = None):
    if tipo_pessoa:
        selected = tipo_pessoa
    else:
        selected = event.widget.get()

    if selected == "Responsável":
        placa_label.place(relx=.5, rely=.2, relwidth=.2, relheight=0.1)
        placa_entry.place(relx=.7, rely=.2, relwidth=.3, relheight=0.1)
    else:
        placa_label.place_forget()
        placa_entry.place_forget()

placa_label = tk.Label(frame_bottom_right_right_bottom, text="Placa")
placa_entry = tk.Entry(frame_bottom_right_right_bottom)

tipo_pessoa_dropdownbox.bind("<<ComboboxSelected>>",select_tipo_pessoa)
tipo_pessoa_dropdownbox.place(relx=.7, rely=.1, relwidth=.3, relheight=0.1)
tipo_pessoa_dropdownbox.update()

table_iid = None
def select_row_pessoas(event):
    if is_to_create or len(event.widget.selection()) == 0:
        return None
    global table_iid
    table_iid = event.widget.selection()[0]
    row = table_pessoas.item(table_iid)['values']
    nome_pessoa.delete(0,tk.END)
    nome_pessoa.insert(0,row[0])
    apartaments_pessoa_dropdownbox.current(row[3])
    nascimento.set_date(row[2])
    tipo_pessoa_dropdownbox.current(next(i for i,res in enumerate(tipo_pessoa) if tipo_pessoa[res] == row[4]))
    select_tipo_pessoa(None, row[4])
    if row[3] == "Responsável":
        pessoa_codigo = database.select(f"select codigo from pessoas where codigo = '{table_iid}'")
        placa_entry.delete(0, tk.END)
        placa_entry.insert(0, database.pessoas_placa[str(pessoa_codigo)])

table_pessoas.bind('<<TreeviewSelect>>', select_row_pessoas)

def create_pessoa():
    global table_iid
    if is_to_create:
        mes,status = database.create_pessoa((nome_pessoa.get(), cpf.get(), apartament_pessoa_selected.get(), nascimento.get_date(), next(chave for chave,valor in tipo_pessoa.items() if valor == pessoa_selected.get()), placa_entry.get()) )
    else:
        mes, status = database.update_pessoa(str(table_iid),nome_pessoa.get(), cpf.get(), apartament_pessoa_selected.get(), nascimento.get_date(), next(chave for chave,valor in tipo_pessoa.items() if valor == pessoa_selected.get()), placa_entry.get())

    show_popup(mes, status)
    refresh_tables()

save_selected = tk.StringVar()
save_selected.set("create")
is_to_create = True
def set_is_to_create(val):
    global is_to_create
    is_to_create = val
    if not is_to_create:
        delete_person.place(relx=.4, rely=.45, relwidth=.3, relheight=0.15)
    else:
        delete_person.place_forget()

def delete_pessoa():
    global table_iid
    if table_iid:
        mes, status = database.delete_pessoa(table_iid)
        refresh_tables()
        show_popup(mes, status)
    else:
        show_popup("Selecione uma pessoa.", 400)

save_option1 = ttk.Radiobutton(frame_bottom_right_right_bottom, text = "Cadastrar", value = "create", variable = save_selected, command=lambda: set_is_to_create(True), takefocus=False)
save_option2 = ttk.Radiobutton(frame_bottom_right_right_bottom, text = "Editar", value = "update", variable = save_selected, command=lambda: set_is_to_create(False), takefocus=False)
delete_person = ttk.Button(frame_bottom_right_right_bottom, text="Excluir", command=delete_pessoa)

save_option1.place(relx = 0.1, rely = 0.3, relwidth = 0.3, relheight = 0.15)
save_option2.place(relx = 0.4, rely = 0.3, relwidth = 0.3, relheight = 0.15)

create_pessoa_button = ttk.Button(frame_bottom_right_right_bottom, text="Salvar", command=create_pessoa)
create_pessoa_button.place(relx=.7, rely=.3, relwidth=.3, relheight=0.15)
create_pessoa_button.update()

frame_camera = tk.Frame(janela, bd=5, relief='ridge',bg='#F7DC6F')
frame_camera.place(relx=.5, rely=0, relwidth=0.5, relheight=0.5)
frame_camera.update()

label = tk.Label(frame_camera, width=frame_camera.winfo_width(), height=frame_camera.winfo_height())
label.place(relx=0, rely=0, relwidth=1, relheight=1)
label.update()

camera = Camera(janela, database, label, refresh_tables)
label.after(0, camera.show_frame)

open_gate = ttk.Button(frame_bottom_right_left_bottom, text="Abrir catraca", command=camera.send_high_esp)
open_gate.place(relx = 0.35, rely = 0.3, relwidth = 0.3, relheight = 0.15)

def update_camera():
    camera.update_camera_database()

janela.minsize(janela_height, janel_width)
janela.mainloop()
database.close()
