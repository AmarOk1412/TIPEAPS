#!/usr/bin/env python2

#Imports
import cv2
import numpy
import time
import os
import sys

#Constantes
TRAINSET = "lbpcascade_frontalface.xml"    #Fichier de reconnaissance
DOWNSCALE = 4                              
IMAGE_SIZE = 170                           #Normalisation des images de base
NUMBER_OF_CAPTURE = 10                     #Nombre de captures à réaliser pour la base de données
SEUIL = 180                                #Seuil de reconnaissance

#####################################



