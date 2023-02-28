import cv2
import pytesseract
import random
import time
from PIL import Image, ImageTk

class Camera():
    def __init__(self, database, label):
        self.database = database
        self.label = label

        res = self.database.select("SELECT * FROM placas_cadastradas")
        self.placas_cadastradas = {placa:{'nome':responsavel, 'codigo':codigo} for codigo, placa, responsavel in res}
        self.passagem_dict = {0:"entrada",1:"saida"}

        #https://github.com/UB-Mannheim/tesseract/wiki
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.capture = cv2.VideoCapture(0)

        self.min_width, self.max_width = 80, 250
        self.plate_ratio = 150/60

    def show_frame(self):
        ret, frame = self.capture.read()
        
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
                if (self.min_width < w and w < self.max_width) and (self.plate_ratio*.9 < aspect_ratio < self.plate_ratio*1.1):  # adiciona apenas retângulos que são menores que os tamanhos máximos especificados
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

            if text in self.placas_cadastradas:     
                t = time.localtime()
                data_passagem = time.strftime("%Y-%m-%d", t)
                horario_passagem = time.strftime("%H:%M:%S", t)
                passagem = int(horario_passagem[-2:]) % 2

                entrada = f"{self.placas_cadastradas[text]['nome']} permitida a {self.passagem_dict[passagem]}."
                cv2.putText(color_gray_frame, entrada, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 1)
                
                sql = "insert into logs(codigo_veiculo, data_passagem, horario_passagem, passagem) values(%s,%s,%s,%s)"
                val = (int(self.placas_cadastradas[text]['codigo']),data_passagem, horario_passagem, self.passagem_dict[passagem])
                self.database.insert(sql, val)

                for tempo in (range(3,0,-1)):
                    cv2.rectangle(color_gray_frame, (0, 0), (100, 40), (0,0,0), -1)
                    cv2.putText(color_gray_frame, f"Aguarde {tempo}s", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 1)
                    #cv2.imshow("Camera2", color_gray_frame)          
                    cv2.waitKey(1000)
        
        if ret:
            cv2.resize(color_gray_frame, (self.label.winfo_width(), self.label.winfo_height()))
            image = Image.fromarray(color_gray_frame)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo
        # Chama esta função novamente em 30 milissegundos
        self.label.after(30, self.show_frame)