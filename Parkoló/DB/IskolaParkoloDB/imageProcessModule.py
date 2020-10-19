import cv2
import numpy as np

from parkingPlace import *

def getGrayDiff(image, lastImage):
    diff1 = cv2.addWeighted(image,1,lastImage,-1,0)
    diff2 = cv2.addWeighted(lastImage,1,image,-1,0)
    diff = cv2.add(diff1,diff2)
    grayDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    asd, thresh = cv2.threshold(grayDiff,10,255,cv2.THRESH_BINARY)

    return thresh

def blackFilter(image, grayImage, value):
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    grayImage2 = grayImage.copy()
    mask = np.where(hsvImage[:,:,2] > value,0,255)

    hsvImage[:,:,2] = mask
    grayImage2[:] = np.where(mask > 120,255,0)

    return grayImage2

def getGroundMask(Width, Height):
    groundMask = np.zeros((Height,Width),np.uint8)

    rectangle = ((427,264),(538,266),(544,293),(460,288))
    ground = parkingPlace(rectangle)
    rect = np.array([ground.corner1,ground.corner2,ground.corner3,ground.corner4])
    cv2.fillConvexPoly(groundMask,rect,255)

    return groundMask
