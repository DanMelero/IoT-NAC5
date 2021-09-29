import cv2
import os
import sys
import os.path
import numpy as np
from matplotlib import pyplot as plt
import math
from functionsWebcam import *

imgOriginal = cv2.imread("circulo.png")

image_da_webcam(imgOriginal)
#---------------------------------------------------------------------

cv2.namedWindow("preview")
# define a entrada de video para webcam
vc = cv2.VideoCapture(0)

#vc = cv2.VideoCapture("video.mp4") # para ler um video mp4

#configura o tamanho da janela
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada
    cv2.imshow("preview", img)
    cv2.imshow("original", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
