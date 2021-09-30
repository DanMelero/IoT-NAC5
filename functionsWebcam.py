#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2
import os,sys, os.path
import numpy as np
from matplotlib import pyplot as plt
import math


def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    img = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask

def set_img (imgHSV):
    imgRGB = cv2.cvtColor(imgHSV, cv2.COLOR_GRAY2RGB)
    imgContornos = imgRGB.copy()
    # contornos, _ = cv2.findContours(imgHSV, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return (imgContornos)


def desenha_cruz(img, cX,cY, size, color):
    cv2.line(img,(cX - size,cY),(cX + size,cY),color,5)
    cv2.line(img,(cX,cY - size),(cX, cY + size),color,5)    

def escreve_texto(img, text, origem, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    origem = (0,50)
    cv2.putText(img, str(text), origem, font,1,color,2,cv2.LINE_AA)

def set_M (array_pos1, array_pos2):
    M = [cv2.moments(array_pos1),  cv2.moments(array_pos2)]
    return M

def centro_de_massa(imgContornos):
    imgCinza = cv2.cvtColor(imgContornos, cv2.COLOR_RGB2GRAY)
    new_contornos, _ = cv2.findContours(imgCinza, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    M = set_M(new_contornos[0], new_contornos[1])
    M1 = M[0]
    M2 = M[1]
    if M1["m00"] != 0 and M2["m00"] != 0:
        M1 = M[0]
        cx1 = int(M1['m10']/M1['m00'])
        cy1 = int(M1['m01']/M1['m00'])

        M2 = M[1]
        cx2 = int(M2['m10']/M2['m00'])
        cy2 = int(M2['m01']/M2['m00'])

    coord = (cx1, cy1, cx2, cy2)

    return coord

def restaurar_original(imgOriginal,imgContorno):
    cl_circulo = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
    bl_circulo = cv2.bitwise_not(imgContorno)
    imgOriRest = cv2.bitwise_or(cl_circulo, bl_circulo)
    return imgOriRest


def validar(imgContornos, coord):
    imgCinza = cv2.cvtColor(imgContornos, cv2.COLOR_RGB2GRAY)
    new_contornos, _ = cv2.findContours(imgCinza, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    menor1 = None
    menor2 = None

    lista = []
    for i in new_contornos:
        area = int(cv2.contourArea(i))
        lista.append(area)
    listaOrdenada = sorted(lista)

    for c in new_contornos:
        area = int(cv2.contourArea(c))
        if listaOrdenada[0] == area:
            menor1 = c
        elif listaOrdenada[1] == area:
            menor2 = c


    M = set_M(new_contornos[0], new_contornos[1])
    M1 = M[0]
    M2 = M[1]

    if M1["m00"] != 0 and M2["m00"] != 0:
        cx1 = int(M1["m10"] / M1["m00"])
        cy1 = int(M1["m01"] / M1["m00"])
        cx2 = int(M2["m10"] / M2["m00"])
        cy2 = int(M2["m01"] / M2["m00"])

        cv2.drawContours(imgContornos, [menor1], -1,[255, 0, 0], thickness=cv2.FILLED)
        cv2.drawContours(imgContornos, [menor2], -1,[255, 0, 0], thickness=cv2.FILLED)

        desenha_cruz(imgContornos, cx1, cy1, 20, (0, 0, 255))
        desenha_cruz(imgContornos, cx2, cy2, 20, (0, 0, 255))

        texto1 = coord[0], coord[1]
        origem1 = (0, 50)

        texto2 = coord[0], coord[1]
        origem2 = (50, 250)

        escreve_texto(imgContornos, texto1, origem1, (0, 255, 0))
        escreve_texto(imgContornos, texto2, origem2, (0, 255, 0))
    else:
        coord[0], coord[1], coord[2], coord[3] = 0, 0
        texto = 'nao tem nada'
        origem = (0, 50)
        escreve_texto(imgContornos, texto, origem, (0, 0, 255))
    return imgContornos

def image_da_webcam(imgOriginal): 

    imgContornos = set_img(filtro_de_cor(
        imgOriginal, np.array([0, 140, 63]), np.array([97, 255, 255])))

    coord = centro_de_massa(imgContornos)

    imgNova = restaurar_original(imgOriginal, coord)

    img = validar(imgNova, coord)
        
    return img
