import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = '0' #webcam externa. Deve vir antes do import cv2

import cv2
import pytesseract
import random

import time
import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('credentials.ini')

db = mysql.connector.connect(
  host=config['credendftials']['host'],
  user=config['credentials']["user"],
  password=config['credentials']['password'],
  database=config['credentials']['database']
)
 
cursor = db.cursor()
query = "SELECT * FROM perfil_cadastrados"
cursor.execute(query)
res = cursor.fetchall()

placas_cadastradas = {placa:{'nome':nome, 'codigo':codigo} for codigo, nome, placa in res}
passagem_dict = {0:"entrada",1:"saida"}
print(placas_cadastradas)

#https://github.com/UB-Mannheim/tesseract/wiki
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
capture = cv2.VideoCapture(0)

min_width, max_width = 80, 250
plate_ratio = 150/60

while True:
  ret, frame = capture.read()
  color_frame = frame.copy()

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
        if (min_width < w and w < max_width) and (plate_ratio*.8 < aspect_ratio < plate_ratio*1.2):  # adiciona apenas retângulos que são menores que os tamanhos máximos especificados
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
  
      if texto in placas_cadastradas:     
        t = time.localtime()
        data_passagem = time.strftime("%Y-%m-%d", t)
        horario_passagem = time.strftime("%H:%M:%S", t)
        passagem = int(horario_passagem[-2:]) % 2

        print(f"{placas_cadastradas[text]['nome']} permitida a {passagem_dict[passagem]}.")

        sql = "insert into logs(nome, placa, data_passagem, horario_passagem, passagem) values(%s,%s,%s,%s,%s)"
        val = (placas_cadastradas[text]['nome'], text, data_passagem, horario_passagem, passagem_dict[passagem])
        cursor.execute(sql, val)
        print("cadastrado")

        time.sleep(5)

  cv2.imshow("Camera2", color_gray_frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):    
    break

db.commit()
db.close()

capture.release()
cv2.destroyAllWindows()
