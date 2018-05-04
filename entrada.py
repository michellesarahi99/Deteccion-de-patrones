from PIL import Image
from os import listdir
import os
from os import listdir
import cv2
import numpy as np

""" Codigo para extraer el color del objeto """

def recorrer(carpetaEntrada, carpetaSalida, imagenes,minNaranja,maxNaranja):
    for nombre in imagenes:
        print (nombre)
        imagen = cv2.imread(carpetaEntrada + "/" +nombre)
        recorte = naranja(imagen,minNaranja,maxNaranja)
        cv2.imwrite(carpetaSalida + "/" + nombre, recorte)

def naranja(imagen,minNaranja,maxNaranja):
    im2 = imagen.copy()
    im3 = imagen.copy()
    im2 = cv2.cvtColor(im2,cv2.COLOR_BGR2HSV)
    cv2.imshow('naranja en hsv', im2)
    cv2.waitKey(0)
    dimMaxima = max(im2.shape)
    escala = 700/dimMaxima
    im2 = cv2.resize(im2, None, fx=escala, fy=escala)
    im3 = cv2.resize(im3, None, fx=escala, fy=escala)
    imagenFiltro = cv2.GaussianBlur(im2, (7, 7), 0)
    cv2.imshow('imagen con filtro gaussian blur', imagenFiltro)
    cv2.waitKey(0)

    mascara = cv2.inRange(imagenFiltro, minNaranja, maxNaranja)
    cv2.imshow('mascara', mascara)
    cv2.waitKey(0)
    """ Morfologia para quitar el ruido
    """
    #Estructura para las transformaciones morfologicas 
    estructura = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #Morfologia close, que elimina puntos negros dentro del objeto
    closeMascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, estructura)
    cv2.imshow('mascara cerrada', closeMascara)
    cv2.waitKey(0)
    #Elimina puntos blancos fuera del objeto
    openMascara= cv2.morphologyEx(closeMascara, cv2.MORPH_OPEN, estructura)
    cv2.imshow('mascara abierta', openMascara)
    cv2.waitKey(0)
    #Funcion que obtiene el contorno de la naranja
    contornoG = contorno(openMascara)
    #Se obtiene una parte del color de la naranja
    recorte= recortar(im3, contornoG)
    return recorte

def contorno(imagen):
	#Se obtienen los contornos de la imagen
    img, contornos, jerarquia = cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #Area de cada contorno
    dimContornos = [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    #Contorno con el area mas grande
    contornoG = max(dimContornos, key=lambda x: x[0])[1]

    #mascara = np.zeros(imagen.shape, np.uint8)
    #cv2.drawContours(mascara, [contornoG], -1, 255, -1)
    return contornoG

def recortar(imagen, contorno):
    imagenCirculo = imagen.copy()
    rectangulo = cv2.fitEllipse(contorno)
    print(rectangulo)
    rx = int((rectangulo[1][0]/3))
    ry = int((rectangulo[1][1]/3))
    x = int(rectangulo[0][0]) - ry
    y = int(rectangulo[0][1]) - rx
    #cv2.ellipse(imagenp, elipse, (0,0,255), 2, cv2.LINE_AA)
    #cv2.imshow('contorno', imagenp)
    #cv2.waitKey(0)
    imagenCirculo = imagenCirculo[y:y+rx*2, x:x+ry*2]
    return imagenCirculo

""" **********************Codigo para extraer los pixeles de la imagen *************"""

def extraerPixeles(ruta, salida):
    #se abre la imagen
    imagen = Image.open(ruta)
    #redimensiona la imagen con ANTIALIS algoritmo con menos perdida
    imagen = imagen.resize((40, 10), Image.ANTIALIAS)

    #carga de pixeles
    pixels = imagen.load()
    #se abre el archivo para lectura escritura
    archivo_entrenamiento = open("datos.csv", "a")
    filas, columnas = imagen.size
    decimales = 4
    for j in range (columnas):
        for i in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            r = str(normalizar(pixels[i,j][0]))
            g = str(normalizar(pixels[i,j][1]))
            b = str(normalizar(pixels[i,j][2]))
            cadena = r[:r.find(".")+decimales] + " " + g[:g.find(".")+decimales] + " " + b[:b.find(".")+decimales] + " "
            archivo_entrenamiento.write(cadena)

    archivo_entrenamiento.write(salida)
    archivo_entrenamiento.write("\n")
    archivo_entrenamiento.close()

def recorrerRecorte(carpetaEntrada, imagenes, salida):
    for nombre in imagenes:
        print(nombre)
        extraerPixeles(carpetaEntrada + "/" +nombre, salida)

def rgbahsv(colores,maxi,mini):
	c = maxi-mini
	h = 0
	v = maxi
	s = c/v
	if(colores[0] == maxi and c != 0):
		h = ((colores[1] - colores[2])/c) % 6
		h = h *60
	if(colores[1] == maxi and c!= 0):
		h = (colores[2]-colores[0])/c + 2
		h = h*60
	if(colores[2] == mini and c != 0):
		h = (colores[0]-colores[1])/c + 4
		h = h*60
	if(c == 0)
		h = 0
	return h,s,v

def normalizar(valor):
    salida = (valor*1.)/255.
    return salida

#Naranja buena
minNaranja = np.array([10, 100, 80])
maxNaranja = np.array([50, 256, 256])
#Naranja verde
minVerde = np.array([30,100,80])
maxVerde = np.array([130,256,256])

minPodrido = np.array([10,80,55])
maxPodrido = np.array([60,256,256])
#recorrer("naranja", "recorte-naranja", listdir("./naranja"),minNaranja,maxNaranja)
#recorrer("naranja-verde", "recorte-verde", listdir("./naranja-verde"),minVerde,maxVerde)
#recorrer("naranja-podrida", "recorte-podrido", listdir("./naranja-podrida"),minPodrido,maxPodrido)
if(os.path.exists("datos.csv")== True):
    os.remove("datos.csv")

recorrerRecorte("recorte-verde", listdir("./recorte-verde"),"1 0 0")
recorrerRecorte("recorte-naranja", listdir("./recorte-naranja"), "0 1 0")
recorrerRecorte("recorte-podrido", listdir("./recorte-podrido"), "0 0 1")