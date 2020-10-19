import cv2
import numpy as np


def maskingRight(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,298),(1280,720),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,237),(71,307),(0,255,0),-1)
    cv2.rectangle(maskedImage,(0,0),(1280,197),(0,255,0),-1)
    cv2.rectangle(maskedImage,(1030,0),(1280,720),(0,255,0),-1)
    triangle = np.array([ [0,0], [0,430], [760,0] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))

    return maskedImage

def maskingLeft(image):
    maskedImage = image.copy()
    cv2.rectangle(maskedImage,(0,430),(1280,720),(0,255,0),-1)
    cv2.rectangle(maskedImage,(690,0),(1280,720),(0,255,0),-1)

    triangle = np.array([ [1280,720], [0,430], [690,0] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))

    triangle = np.array([ [0,0], [0,300], [780,0] ], np.int32)
    cv2.fillConvexPoly(maskedImage,triangle,(0,255,0))

    return maskedImage
    
