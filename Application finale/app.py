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
import math
import serial

#Constantes
TRAINSET = "lbpcascade_frontalface.xml"    #Fichier de reconnaissance
IMAGE_SIZE = 170                           #Normalisation des images de base
NUMBER_OF_CAPTURE = 10                     #Nombre de captures a realiser pour la base de donnees
SEUIL = 90                                 #Seuil de reconnaissance
CAMERA = 0                                 #La camera

INDIVIDUS = []

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
        faces = self.classifier.detectMultiScale(frame)
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
        #On met l'image en niveaux de gris. TODO: gradient
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
            #Affichage du texte
            cv2.putText(frame, "Appuyez sur c pour collecter", (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0))
            cv2.imshow("Create Database Window", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break
            if key in [ord('C'), ord('c')] and self.faceFrame != None: 
                self.collectFace(self.faceFrame)

class Recognize():
    def __init__(self, imgPath):
        self.rval = False            
        self.camera = cv2.VideoCapture(CAMERA)
        self.classifier = cv2.CascadeClassifier(TRAINSET)
        self.faceFrame = None
        self.identities = []
        self.imagesPath = imgPath
        self.images = []
        self.imagesIndex = []
        self.time = time.time()

    def getFacesPos(self, frame):
        """Retourne la position des visages détéctés de la forme [[x y w h]]"""
        faces = self.classifier.detectMultiScale(frame)
        return faces

    def drawDetected(self, frame, detected, color):
        """Dessine un rectangle autour du visage détecté"""
        if detected is None:
            return frame
        for d in detected: 
            x,y,w,h = [v for v in d]
            cv2.rectangle(frame, (x,y), (x+w, y+h), color)
        return frame

    def getFaceFrame(self, frame, x, y, w, h):
        """On récupère un rectangle (largeur, hauteur) (centreX, centreY)"""
        cropped = cv2.getRectSubPix(frame, (w, h), (x + w / 2, y + h / 2))
        #On met l'image en niveaux de gris. TODO: embossage
        grayscale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        self.faceFrame = cv2.resize(grayscale, (IMAGE_SIZE, IMAGE_SIZE))
        return self.faceFrame
   
    def extractAndResize(self, frame, x, y, w, h):
        """On récupère juste la tête en noir et blanc"""
        cropped = cv2.getRectSubPix(frame, (w, h), (x + w / 2, y + h / 2))
        grayscale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(grayscale, (IMAGE_SIZE, IMAGE_SIZE))
        return resized

    def readImages(self):
        """Récupère les images de bases pour effectuer la reconnaissance des visages"""
        c = 0
        self.images = []
        self.imagesIndex = []
        for dirname, dirnames, filenames in os.walk(self.imagesPath):
            for subdirname in dirnames:
                self.identities.append(subdirname)
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    try:
                        im = cv2.imread(os.path.join(subject_path, filename), 0)
                        self.images.append(numpy.asarray(im, dtype=numpy.uint8))
                        self.imagesIndex.append(c)
                    except IOError, (errno, strerror):
                       print "I/O error({0}): {1}".format(errno, strerror)
                    except:
                        print "Unexpected error:", sys.exc_info()[0]
                        raise
                c += 1 

    def recognizeLBPHFace(self):
        """Reconnait par la méthode LBPH"""
        self.model = cv2.createLBPHFaceRecognizer()        
        self.model.train(numpy.asarray(self.images), numpy.asarray(self.imagesIndex))

    def recognize(self):
        """On choisit la méthode de reconnaissance et on construit la base de donnée"""
        self.readImages()
        self.recognizeLBPHFace()
        if not self.camera.isOpened():
            return
        self.capture()
    
    def identify(self, image):
        """On reconnaît l'identité de la personne si enregistrée"""
        [p_index, p_confidence] = self.model.predict(image)
        found_identity = self.identities[p_index]
        return found_identity, p_confidence

    def capture(self): 
        """Récupère le flux vidéo"""
        intervalle = 0
        if self.camera.isOpened():
            (rval, frame) = self.camera.read()
        else:
            rval = False
        i = 0
        while i < 105:
            i+=1
            (rval, frame) = self.camera.read()
            self.time = time.time()
            facePos = self.getFacesPos(frame)
            frame = self.drawDetected(frame, facePos, (0,140,255))
            for f in facePos: 
                x,y,w,h = [v for v in f]
                resized = self.extractAndResize(frame, x, y, w, h)
                identity, confidence = self.identify(resized)
                if confidence > SEUIL:
                    identity = "INCONNU"
                INDIVIDUS.append(identity)
                print(identity + " --- " + str(confidence))
                cv2.putText(frame, "%s (%s)"%(identity, confidence), (x,y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,140,255))
            cv2.imshow("Indentification", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600)  
    recognize = Recognize("images")
    recognize.recognize()
    #TODO : Améliorer la condition
    if len(INDIVIDUS) > 50: #and INDIVIDUS.count(INDIVIDUS[0]) > 50:
        print('Bienvenue ' + INDIVIDUS[0])
        ser.write('e')
