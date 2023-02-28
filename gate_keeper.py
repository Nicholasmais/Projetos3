import tkinter as tk
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

frame_inputs = tk.Frame(janela, bd=5, relief='ridge', width=int(janel_width*.8), height=janela_height/2)
frame_inputs.place(x=int(janel_width*.1), y=janela_height/2)

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
input_data.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.1)

button = tk.Button(frame_inputs, text="Dia específico", command=lambda:passage_num_plot(database, canvas, ax, input_data.get_date()))
button.place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.1)
button = tk.Button(frame_inputs, text="Todos os dias", command=lambda:passage_num_plot(database, canvas, ax, ''))
button.place(relx=0.2, rely=0.2, relwidth=0.1, relheight=0.1)

janela.minsize(janela_height, janel_width)
janela.mainloop()
database.close()
