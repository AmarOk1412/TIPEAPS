#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
    def __init__(self, imgPath ,ident):
        self.rval = False            
        self.camera = cv2.VideoCapture(CAMERA)
        self.classifier = cv2.CascadeClassifier(TRAINSET)
        self.faceFrame = None
        self.identity = ident
        self.imagesPath = imgPath

    def getFacesPos(self, frame):
        """Retourne la position des visages détéctés de la forme [[x y w h]]"""
        Size = (frame.shape[1], frame.shape[0])
        miniature = cv2.resize(frame, Size)
        faces = self.classifier.detectMultiScale(miniature)
        return faces

    def drawDetectedFace(self, frame, faces):
        """Dessine un rectangle autour du visage détecté"""
        for f in faces: 
            x,y,w,h = [v for v in f]
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,140,255))
            self.LBPHBaseImage = self.getFaceFrame(frame, x, y, w, h)
        return frame

    def getFaceFrame(self, frame, x, y, w, h):
        """On récupère un rectangle (largeur, hauteur) (centreX, centreY)"""
        cropped = cv2.getRectSubPix(frame, (w, h), (x + w / 2, y + h / 2))
        #On met l'image en niveaux de gris. TODO: relief
        grayscale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #hsvMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        #hlsMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2HLS)
        #luvMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2LUV)
        #labMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2LAB)
        self.faceFrame = cv2.resize(grayscale, (IMAGE_SIZE, IMAGE_SIZE))
        return self.faceFrame

    def collectFace(self, frame):
        """On enregistre le visage récupéré"""     
        imageCreated = False
        captureNum = 0
        #Créé le dossier s'il n'existe pas
        try:
            os.makedirs("{0}/{1}".format(self.imagesPath, self.identity))
        except OSError:
            print("écriture dans dossier existant") 
        #Créé l'image à la suite
        while not imageCreated:
            if not os.path.isfile("{0}/{1}/{2}.jpg".format(self.imagesPath, self.identity, captureNum)):
                cv2.imwrite("{0}/{1}/{2}.jpg".format(self.imagesPath, self.identity, captureNum), frame)
                imageCreated = True
            else:
                captureNum += 1

    def capture(self): 
        """Récupère le flux vidéo"""       
        if self.camera.isOpened():
            (rval, frame) = self.camera.read()
        else:
            rval = False

        while rval:
            (rval, frame) = self.camera.read()
            frame = self.drawDetectedFace(frame, self.getFacesPos(frame))
            cv2.imshow("Create Database Window", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break
            if key in [ord('C'), ord('c')] and self.faceFrame != None: 
                self.collectFace(self.faceFrame)
        

#class RecognizeEigenFaces():
#    def __init__(self):
#        self.camera = CAMERA

#class RecognizeLPBH():
#    def __init__(self):
#        self.camera = CAMERA

if __name__ == "__main__":
    individu = "User"
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-n' and i < len(sys.argv):
            individu = sys.argv[i + 1]
    createDB = CreateDataBase("image", individu)
    createDB.capture()



