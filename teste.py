#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2
import os
import sys
import os.path
import numpy as np

#filtro baixo
# image_lower_hsv1 = np.array([0, 142, 84])
# image_upper_hsv1 = np.array([18, 205, 255])
image_lower_hsv1 = np.array([0, 130, 190])
image_upper_hsv1 = np.array([10, 255, 255])

#filtro alto
# image_lower_hsv2 = np.array([70, 160, 114])
# image_upper_hsv2 = np.array([100, 205, 255])
image_lower_hsv2 = np.array([163, 232, 137])
image_upper_hsv2 = np.array([10, 255, 255])

def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada"""
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask


def mascara_or(mask1, mask2):
    """ retorna a mascara or"""
    mask = cv2.bitwise_or(mask1, mask2)
    return mask


def mascara_and(mask1, mask2):
    """ retorna a mascara and"""
    mask = cv2.bitwise_and(mask1, mask2)
    return mask


def desenha_cruz(img, cX, cY, size, color):
    """ faz a cruz no ponto cx cy"""
    cv2.line(img, (cX - size, cY), (cX + size, cY), color, 5)
    cv2.line(img, (cX, cY - size), (cX, cY + size), color, 5)


def escreve_texto(img, text, origem, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    origem = (0, 50)
    cv2.putText(img, str(text), origem, font, 1, color, 2, cv2.LINE_AA)

def image_da_webcam(img):
    mask_hsv1 = filtro_de_cor(img, image_lower_hsv1, image_upper_hsv1)
    mask_hsv2 = filtro_de_cor(img, image_lower_hsv2, image_upper_hsv2)

    mask_hsv = mascara_or(mask_hsv1, mask_hsv2)

    contornos, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB)
    contornos_img = mask_rgb.copy()

    menor1 = None
    menor2 = None
    menor3 = None
    menor4 = None

    lista = []
    for i in contornos:
        area = int(cv2.contourArea(i))
        lista.append(area)
    listaOrdenada = sorted(lista)

    for c in contornos:
        area = int(cv2.contourArea(c))
        if listaOrdenada[0] == area:
            menor1 = c
        elif listaOrdenada[1] == area:
            menor2 = c
        elif listaOrdenada[2] == area:
            menor3 = c
        else:
            menor4 = c
    M1 = cv2.moments(menor1)
    M2 = cv2.moments(menor2) 
    M3 = cv2.moments(menor3)
    M4 = cv2.moments(menor4)

    # Verifica se existe alguma para calcular, se sim calcula e exibe no display
    if M1["m00"] != 0 and M2["m00"] != 0:
        cv2.drawContours(contornos_img, [menor1], -1, [0, 0, 255], thickness=cv2.FILLED)
        cv2.drawContours(contornos_img, [menor2], -1, [0, 0, 255], thickness=cv2.FILLED)
    
    elif M3["m00"] != 0 and M4["m00"] != 0:
        cX3 = int(M3["m10"] / M3["m00"])
        cY3 = int(M3["m01"] / M3["m00"])
        cX4 = int(M4["m10"] / M4["m00"])
        cY4 = int(M4["m01"] / M4["m00"])

        cv2.drawContours(contornos_img, [menor3], -1, [0, 255, 0], 5)
        cv2.drawContours(contornos_img, [menor4], -1, [0, 255, 0], 5)


        #faz a cruz no centro de massa
        desenha_cruz(contornos_img, cX3, cY3, 20, (0, 0, 255))
        desenha_cruz(contornos_img, cX4, cY4, 20, (0, 0, 255))

        # Para escrever vamos definir uma fonte
        texto3 = cY3, cX3
        origem3 = (0, 50)

        texto4 = cY4, cX4
        origem4 = (0, 50)

        escreve_texto(contornos_img, texto3, origem3, (0, 255, 0))
        escreve_texto(contornos_img, texto4, origem4, (0, 255, 0))

        coord3 = (cX3, cY3)
        coord4 = (cX4, cY4)
        cv2.line(contornos_img, coord3, coord4, (0, 0, 255), 4)

    else:
        cX3, cY3, cX4, cY4 = 0, 0, 0, 0
        # Para escrever vamovpn definir uma fonte
        texto = 'nao encontrado'
        origem = (0, 50)
        escreve_texto(contornos_img, texto, origem, (180, 100, 180))

    return contornos_img


cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)

# vc = cv2.VideoCapture("teste.mp4") # para ler um video mp4

vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened():  
    rval, frame = vc.read()
else:
    rval = False

while rval:

    # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada
    img = image_da_webcam(frame)

    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
