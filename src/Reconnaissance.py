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
            #Affichage du texte
            cv2.putText(frame, "Appuyez sur c pour collecter", (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0))
            cv2.imshow("Create Database Window", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break
            if key in [ord('C'), ord('c')] and self.faceFrame != None: 
                self.collectFace(self.faceFrame)

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

    def getFacesPos(self, frame):
        """Retourne la position des visages détéctés de la forme [[x y w h]]"""
        faces = self.classifier.detectMultiScale(frame)
        return faces


    def getMouthPos(self, frame, facePos):
        #TODO:Meilleur classifier, la c'est merdique
        """Retourne la position des bouches détéctés de la forme [[x1 y1 x2 y2]]"""        
        if len(facePos) > 0:
            cascade = cv2.CascadeClassifier('mouth_classifier.xml')
            rects = cascade.detectMultiScale(frame)        
            if len(rects) == 0:
                return rects
            final = None   
            x1 = facePos[0][0]
            x2 = facePos[0][0] + facePos[0][2]
            y1 = facePos[0][1] + facePos[0][3]*5/8
            y2 = facePos[0][1] + facePos[0][3]
            #Prend la partie inférieure de la tête pour le traitement
            for rect in rects:
                if rect[0] > x1 and rect[0] + rect[2] < x2 and rect[1] > y1 and rect[1] + rect[3] < y2:
                    if final is None:
                        final = [rect]
                    else:
                        final += [rect]
            return final
        else:
            return None

    def getEyesPos(self, frame):
        """Retourne la position des yeux + sourcils détéctés de la forme [[x1 y1 x2 y2]]"""
        cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')
        rects = cascade.detectMultiScale(frame)
        return rects

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
        #On met l'image en niveaux de gris. TODO: relief
        grayscale = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #hsvMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
        #hlsMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2HLS)
        #luvMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2LUV)
        #labMode = cv2.cvtColor(cropped, cv2.COLOR_BGR2LAB)
        self.faceFrame = cv2.resize(grayscale, (IMAGE_SIZE, IMAGE_SIZE))
        return self.faceFrame

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

    def recognizeEigenFace(self, frame):
        """Reconnait par la méthode EigenFace"""
        self.model = cv2.createEigenFaceRecognizer()
        #TODO : créer la base d'entrainement + méthode identify self.model.train(numpy.asarray(self.images), numpy.asarray(self.images_index))

   #TODO : Fisherface + LBPH

    def cropFromFace(self, frame, facePos):
        """garde seulement la partie "tête" de la frame"""
        #X,Y,W,H
        if len(facePos) == 0 :
            return frame
        else :
            x1 = facePos[0][0]
            x2 = x1 + facePos[0][2]
            y1 = facePos[0][1]
            y2 = y1 + facePos[0][3]
            return frame[y1:y2, x1:x2]

    def capture(self): 
        """Récupère le flux vidéo"""
        self.readImages()       
        if self.camera.isOpened():
            (rval, frame) = self.camera.read()
        else:
            rval = False

        while rval:
            (rval, frame) = self.camera.read()
            facePos = self.getFacesPos(frame)
            cropped = self.cropFromFace(frame, facePos)
            frame = self.drawDetected(frame, facePos, (0,140,255))
            frame = self.drawDetected(frame, self.getEyesPos(frame), (255,0,255))
            frame = self.drawDetected(frame, self.getMouthPos(frame, facePos), (0,0,255))
            cv2.imshow("Create Database Window", frame)
            key = cv2.waitKey(20)
            if key in [27, ord('Q'), ord('q')]: #esc / Q
                break

#class RecognizeLPBH():
#    def __init__(self):
#        self.camera = CAMERA

if __name__ == "__main__":
    individu = "User"
    mode = 0
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-n' and i < len(sys.argv):
            individu = sys.argv[i + 1]
        if sys.argv[i] == '-r':
            mode = 1
    if mode == 0:
        createDB = CreateDataBase("image", individu)
        createDB.capture()
    else:
        recognize = Recognize("image", individu)
        recognize.capture()



