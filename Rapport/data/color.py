import numpy as np
import cv2

im = cv2.imread('test.png')
# Convertit une image RGB en HSV
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

# Defini la plage de couleurs a detecter
lower_blue = np.array([120, 0,50])
upper_blue = np.array([140,100,100])

# Realise un mask avec la plage donnee
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Enregistre l'image apres avoir realise le masque
res = cv2.bitwise_and(im,im, mask= mask)
cv2.imwrite('fincolor.jpg',res)

#Realisation masque sur une image en noir et blanc (ici les gris entre 50 et 255)
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
cv2.imwrite('finnb.png',thresh)
