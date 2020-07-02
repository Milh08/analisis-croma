# -*- coding: utf-8 -*-
"""Circulos6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11k_X_wXgjwPndpbmM21LnUbVPM5gX_74
"""

import cv2
import numpy as np

class Deteccion_del_Croma():

  def Definir_Area(self, nombre_de_la_imagen):

    # ------------------- Inicio para la deteccion del contorno del croma --------------------------

    URL = "uploads/" + nombre_de_la_imagen # Ruta de la imagen en el directorio del sistema

    img = cv2.imread(URL) # Se hace lectura de la imagen

    # ---------- Redimencionar imagen --------------
    porcentaje_escala = 50
    Altura = int(img.shape[0] * porcentaje_escala / 100) 
    Ancho  = int(img.shape[1] * porcentaje_escala / 100)

    nuevo_Tamaño = (Ancho, Altura)

    if img.shape[0] > 1500 and img.shape[1] > 1500:
      img = cv2.resize(img, nuevo_Tamaño)
    # ---------- fin de la redimencion -------------

    img2 = img.copy() # Se hace una copia de la imagen

    img = cv2.medianBlur(img, 67) # Se aplica un flitro a la imagen para quitar el ruido
    img[np.all(img >= 225, axis=2)] = 0 # Permite a la imagen que elimine los colores blancos de la imagen

    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Convertimos la imagen a escala de grices
    _, bw = cv2.threshold(bw, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # Hacemos que la imagen sea binaria

    kernel = np.ones((3,3),np.uint8) 

    # Esta operacion morfologica permite el cierre los pequeños 
    # agujeros dentro de la imagen
    opening = cv2.morphologyEx(bw,cv2.MORPH_CLOSE,kernel, iterations = 2) 
    opening = cv2.medianBlur(opening, 33) # Se aplica un flitro a la imagen para quitar el ruido

    cnts,_ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Se buscan los contornos de cada parte de la imagen

    areas = [] # Array donde se almacenaran el area de cada contorno
    for con in cnts:
      area = cv2.contourArea(con) # Permite obtener el area de cada contorno
      areas.append(area) # Cada area se agrega al array

    posicion_de_contorno_del_Circulo = areas.index(max(areas)) # Se obtine la pocicion del AREA mas grande
    contorno_del_circulo = cnts[posicion_de_contorno_del_Circulo] # Se obtine el contorno con el area mas grande

    # Dimenciones de la imagen x --> Inicio del contorno en el eje X, 
    # y --> Inicio del contorno en el eje y, w --> ancho del area de la imagen, 
    # h --> altura del area de la imagen
    x,y,w,h  = cv2.boundingRect(contorno_del_circulo) 

    M = cv2.moments(contorno_del_circulo) # Permitira encontrar en centro del area

    if (M["m00"]==0):M["m00"] = 1 # Se convierte a 1 para que se permita la divicion
    xcentro = int(M["m10"]/M["m00"]) # Se encuentra el centro en el eje X
    ycentro = int(M["m01"]/M["m00"]) # Se encuentra el centro en el eje Y
    radio   = xcentro-x

    cv2.circle(img2, (x, ycentro), 3, (0,0,255), -1) # Permite dejar una marca en la orilla del area

    Fila_a_Buscar = int(img.shape[0]/2) # Fila donde se buscara la marca en la orilla del area

    # -------------------------- Fin de la deteccion del contorno del croma ---------------------

    # ------------------- Inicio de la convercio de carteciano a polar de la imagen --------------------

    img3 = img2.astype(np.float32) # Los valores de la imagen 2 se cambian a valores glotantes (1) --> (1.0)
    value = np.sqrt((ycentro**2.0)+(xcentro**2.0))

    polar_img = cv2.linearPolar(img3, (xcentro, ycentro), value, cv2.WARP_FILL_OUTLIERS) # Convercion de la imagen a Polar
    polar_img = polar_img.astype(np.uint8) # Convercion de valores de flotante a enteres (1.0) --> (1)

    columna_a_cortar = 0
    for p in range(0, len(polar_img[Fila_a_Buscar])):
      color_rojo = np.array([0, 0, 255]) # Color que se busca en la imagen

      if np.array_equal(polar_img[Fila_a_Buscar][p], color_rojo): # Se compara si el valor en el pixcel es igual a la del color buscado
        columna_a_cortar = p # Se asigna la posicion de la columna donde de encontro el color
        break
    
    polar_img = polar_img[0:polar_img.shape[0] , 0:columna_a_cortar] # Se corta la imagen donde no es util

    horizontal_img = cv2.rotate(polar_img, cv2.ROTATE_90_CLOCKWISE) # Se ajusta la imagen de modo que los picos esten hacia abajo

    cv2.imwrite(URL, horizontal_img)
    # ------------------ Fin del la conversion de carteciano a polar ------------------------------

    return horizontal_img

# Croma = Deteccion_del_Croma()

# img = Croma.Definir_Area('1')

# mostrar = cv2.resize(img, (900,650))
# cv2_imshow(mostrar)