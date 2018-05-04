import cv2
import numpy as np
import os
from PIL import Image
import neurolab as nl
import scipy as sp

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
    #Colores maximos y minimos donde la naranja está buena

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
    #rectangulo_tomate = cv2.resize(rectangulo_tomate, (100, 50))
    # recortar(rectangulo_tomate)
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
    rx = int((rectangulo[1][0]/3))
    ry = int((rectangulo[1][1]/3))
    x = int(rectangulo[0][0]) - ry
    y = int(rectangulo[0][1]) - rx
    #cv2.ellipse(imagenp, elipse, (0,0,255), 2, cv2.LINE_AA)
    #cv2.imshow('contorno', imagenp)
    #cv2.waitKey(0)
    imagenCirculo = imagenCirculo[y:y+rx*2, x:x+ry*2]
    return imagenCirculo

def extraerPixeles(imagen):
    #rangos de color para estimar la madurez
    minNaranjaRGB = np.array([204,34,0])
    maxNaranjaRGB = np.array([255,213,0])

    im = Image.open(imagen)
    im = im.resize((40, 10), Image.ANTIALIAS)
    grado = 0
    muestra = 0
    brillo = 0
    hsv = rgbahsv(maxNaranjaRGB)
    pixels = im.load()
    pixeles = pixels
    fila,columna = im.size

    for i in range(fila):
        for j in range(columna):
            muestra = muestra + int(pixels[i,j][0])

    for i in range(fila):
        for j in range(columna):
            hsv2 = rgbahsv(pixeles[i,j])
            brillo = brillo + hsv2[2]

    grado = ((muestra/400) *  100)/maxNaranjaRGB[0]
    calidad = ((brillo/400)) * 100/ hsv[2]
    #print("Pixel", pix)
    filas, columnas = im.size
    decimales = 4
    cadena = ""
    for columna in range (columnas):
        for fila in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            rojo = str(normalizar(pixels[fila,columna][0]))
            verde = str(normalizar(pixels[fila,columna][1]))
            azul = str(normalizar(pixels[fila,columna][2]))
            cadena = cadena + rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "

    return cadena, grado, brillo

def rgbahsv(colores):
    maxi = colores[0]
    mini = colores[0]
    for i in range(len(colores)-1):
        if(maxi < colores[i+1]):
            maxi = colores[i+1]
    for i in range(len(colores)-1):
        if(mini > colores[i+1]):
            mini = colores[i +1]
    hsv = []
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
    if(c == 0):
        h = 0
    hsv.append(h)
    hsv.append(s)
    hsv.append(v)
    return hsv

def normalizar(valor):
    salida = (valor*1.)/255.
    return salida


#Naranja buena
minNaranja = np.array([10, 100, 80])
maxNaranja = np.array([50, 256, 256])
#Naranja verde
minVerde = np.array([30,100,80])
maxVerde = np.array([130,256,256])
#Naranja Podrida
minPodrido = np.array([10,80,55])
maxPodrido = np.array([60,256,256])

imagen = cv2.imread("prueba2.jpg")

imagen = naranja(imagen,minNaranja,maxNaranja)
#imagen = naranja(imagen,minVerde,maxVerde)
#imagen = naranja(imagen,minPodrido,maxPodrido)

cv2.imwrite("naranja-recortada.jpg",imagen)

cadena, gradoMadurez, calidad = extraerPixeles("naranja-recortada.jpg")

if(os.path.exists("dato-prueba.csv")== True):
    os.remove("dato-prueba.csv")

archivo = open("dato-prueba.csv", "a")

archivo.write(cadena)
archivo.close()

datos = np.matrix(sp.genfromtxt("dato-prueba.csv", delimiter=" "))
matiz = 0
i = 0
#while(i != 1200):
 #   matiz = matiz + datos[0][i]
 #   i = i + 3
#print (datos.shape)

rna = nl.load("red-entrenada.tmt")

salida = rna.sim(datos)
verde = salida[0][0] * 100
maduro = salida[0][1] * 100
podrido = salida[0][2] * 100

resultado = ""
if(gradoMadurez <= 30):
    print("Su tiempo estimado de vida es: 7 días")
if(gradoMadurez >= 31 and gradoMadurez <= 60):
    print("Su tiempo estimado de vida es: 4 días")
if(gradoMadurez >= 61 and gradoMadurez <= 85):
    print("Su tiempo estimado de vida es : 2 días")
if(gradoMadurez >= 86 and gradoMadurez <= 100):
    print("La naranja ya caducó")
gradoMadurez = str(gradoMadurez)
calidad = str(calidad)

if (podrido > 80.):
    resultado = "La naranja esta podrida"

if (maduro > 80.):
    resultado = "La naranja esta madura"
    print("El grado de madurez de la naranja es de: ", gradoMadurez[:gradoMadurez.find(".") + 3], " %")
if (verde > 80.):
    resultado = "La naranja esta verde"
    print("El grado de madurez de la naranja es de: ", gradoMadurez[:gradoMadurez.find(".") + 3], " %")

print (resultado)

print("")
print("La calidad de la naranja es: ", calidad[:calidad.find(".") + 3], " %")