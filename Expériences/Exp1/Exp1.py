import cv2, cv, sys
import numpy as np

individu = sys.argv[1]
print('bonjour ' + individu)
cap = cv2.VideoCapture(0)

i=0
aff = False
while(i <= 106):

    # Take each frame
    _, frame = cap.read()
    if i < 12 and aff:
        print('Prendre 12 photos de bases assez differentes')
        aff = False
    if i < 17 and aff:
        print('Regarder 5 points en neutre (haut bas gauche droite milieu)')
        aff = False
    if i < 23 and aff:
        print('Regarder 5 points en surpris (haut bas gauche droite milieu)')
        aff = False
    if i < 28 and aff:
        print('Regarder 5 points en yeux fermes (haut bas gauche droite milieu)')
        aff = False
    if i < 34 and aff:
        print('Regarder 5 points en sourire (haut bas gauche droite milieu)')
        aff = False
    if i < 40 and aff:
        print('Regarder 5 points en enerve (haut bas gauche droite milieu)')
        aff = False
    if i < 46 and aff:
        print('Regarder 5 points en grimaces (haut bas gauche droite milieu)')
        aff = False
    cv2.imshow('frame',frame)
    if i >= 6:
        cv.SaveImage('images/picDef' + individu + str(i-6) + '.png', cv.fromarray(frame))#Changer picDef par picCache
    key = cv2.waitKey(20)
    i += 1
    if key in [ord('C'), ord('c')]:          
        aff = True

cv2.destroyAllWindows()
