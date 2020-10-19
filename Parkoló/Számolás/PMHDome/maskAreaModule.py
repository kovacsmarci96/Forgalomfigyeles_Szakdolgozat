import cv2
import numpy as np

from parkingPlace import *

def maskBig(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,0),(1280,106),(0,255,0),-1)
    triangle = np.array([ [0,106], [697,106], [0,733] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))
    triangle = np.array([ [267,475], [720,720], [0,720] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))
    rectangle = np.array([ [999,107], [967,720], [1280,720], [1280,106] ], np.int32)
    cv2.fillConvexPoly(maskedImage,rectangle,(0,255,0))

    return maskedImage

def maskSmall(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,0),(1280,154),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,275),(1280,720),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,160),(1130,392),(0,255,0),-1)

    return maskedImage

def getGroundMask(Width, Height):
    groundMask = np.zeros((Height,Width),np.uint8)

    rectangle = ((885, 479),(967, 497),(989, 338),(923, 324))

    ground = parkingPlace(rectangle)

    rect = np.array([(ground.corner1,ground.corner2,ground.corner3,ground.corner4)])
   
    cv2.fillConvexPoly(groundMask,rect,255)

    return groundMask
