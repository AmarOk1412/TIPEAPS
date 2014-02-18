#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Imports
import cv2
import numpy
import time
import os
import sys
import math

#Constantes
TRAINSET = "lbpcascade_frontalface.xml"    #Fichier de reconnaissance
IMAGE_SIZE = 170                           #Normalisation des images de base
NUMBER_OF_CAPTURE = 10                     #Nombre de captures a realiser pour la base de donnees
SEUIL = 4000                               #Seuil de reconnaissance
CAMERA = 0                                 #La camera

class Recognize():
    def __init__(self, imgPath ,ident):
        self.rval = False            
        self.camera = cv2.VideoCapture(CAMERA)
        self.classifier = cv2.CascadeClassifier(TRAINSET)
        self.faceFrame = None
        self.identity = ident
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

    def recognizeFisherFace(self):
        """Reconnait par la méthode EigenFace"""
        self.model = cv2.createFisherFaceRecognizer()        
        self.model.train(numpy.asarray(self.images), numpy.asarray(self.imagesIndex))
        #TODO : créer la base d'entrainement + méthode identify self.model.train(numpy.asarray(self.images), numpy.asarray(self.imagesIndex))
    
    def recognizeEigenFace(self):
        """Reconnait par la méthode EigenFace"""
        self.model = cv2.createEigenFaceRecognizer()        
        self.model.train(numpy.asarray(self.images), numpy.asarray(self.imagesIndex))

    def recognizeLBPHFace(self):
        """Reconnait par la méthode EigenFace"""
        self.model = cv2.createLBPHFaceRecognizer()        
        self.model.train(numpy.asarray(self.images), numpy.asarray(self.imagesIndex))

    def recognize(self):
        """On choisit la méthode de reconnaissance et on construit la base de donnée"""
        self.time = time.time()
        self.readImages()
        self.recognizeEigenFace()
        #self.recognizeFisherFace()
        #self.recognizeLBPHFace()
        print('L\'ajout des images dans la bdd a pris : ' +str(time.time()- self.time))
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
        self.readImages()
        intervalle = 0
        if self.camera.isOpened():
            (rval, frame) = self.camera.read()
        else:
            rval = False

        while rval:
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
                print('La reconnaissance a pris : ' +str(time.time()- self.time))
                self.time = time.time()
                cv2.putText(frame, "%s (%s)"%(identity, confidence), (x,y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,140,255))
            cv2.imshow("Indentification", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break

if __name__ == "__main__":
    individu = "User"
    mode = 0
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-n' and i < len(sys.argv):
            individu = sys.argv[i + 1]
        if sys.argv[i] == '-r':
            mode = 1
    recognize = Recognize("images", individu)
    recognize.recognize()
