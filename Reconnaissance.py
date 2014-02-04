#!/usr/bin/env python2

#   ooooooooooo ooooo oooooooooo ooooooooooo      o      oooooooooo   oooooooo8  
#   88  888  88  888   888    888 888            888      888    888 888         
#       888      888   888oooo88  888ooo8       8  88     888oooo88   888oooooo  
#       888      888   888        888          8oooo88    888                888 
#      o888o    o888o o888o      o888ooo8888 o88o  o888o o888o       o88oooo888

#Imports
import cv2
import numpy
import time
import os
import sys

#Constantes
TRAINSET = "lbpcascade_frontalface.xml"    #Fichier de reconnaissance
IMAGE_SIZE = 170                           #Normalisation des images de base
NUMBER_OF_CAPTURE = 10                     #Nombre de captures a realiser pour la base de donnees
SEUIL = 180                                #Seuil de reconnaissance
CAMERA = 0                                 #La camera

#####################################
class CreateDataBase():
    def __init__(self):
        self.rval = False            
        self.camera = cv2.VideoCapture(CAMERA)

    def capture(self):        
        if self.camera.isOpened():
            (rval, frame) = self.camera.read()
        else:
            rval = False

        while rval:
            (rval, frame) = self.camera.read()
            cv2.imshow("Create Database Window", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break
        

#class RecognizeEigenFaces():
#    def __init__(self):
#        self.camera = CAMERA

#class RecognizeLPBH():
#    def __init__(self):
#        self.camera = CAMERA

if __name__ == "__main__":
    createDB = CreateDataBase()
    createDB.capture()	



