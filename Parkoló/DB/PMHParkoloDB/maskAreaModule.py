import cv2
import numpy as np

from parkingPlace import *

def maskMiddle(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,0),(1920,352),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,1080),(1920,630),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,352),(570,630),(0,255,0),-1)
    triangle = np.array([ [1263,630], [1490,502], [1489,630] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))
    triangle = np.array([ [565,430], [898,352], [572,352] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))
    cv2.rectangle(maskedImage,(1489,352),(1920,630),(0,255,0),-1)
    triangle = np.array([ [664,395], [1176,342], [848,273] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))

    triangle = np.array([ [570,428], [824,631], [568,631] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))
    
    return maskedImage

def maskFront(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,0),(1920,577),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,0),(815,1052),(0,255,0),-1)
    triangle = np.array([ [816,950], [1708,573], [816,577] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))

    return maskedImage

def maskBack(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,0),(1920,314),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,534),(1920,1080),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,315),(341,534),(0,255,0),-1)
    cv2.rectangle(maskedImage,(1106,315),(1920,534),(0,255,0),-1)
    triangle = np.array([ [1106,350], [342,534], [1104,534] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))

    return maskedImage

def getGroundMask(Width, Height):
    groundMask = np.zeros((Height,Width), np.uint8)

    rectangle = ((1156,525),(1050,589),(1122,627),(1258,541))

    ground = parkingPlace(rectangle)

    rect = np.array([ground.corner1, ground.corner2, ground.corner3, ground.corner4])

    cv2.fillConvexPoly(groundMask, rect, 255)


    return groundMask
    
