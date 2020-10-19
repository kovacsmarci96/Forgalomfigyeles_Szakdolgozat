import cv2
import numpy as np

Width = 1920
Height = 1080

def backgroundSubstraction(frame, fgbg = cv2.createBackgroundSubtractorMOG2()):
    mask = fgbg.apply(frame)
    return mask

def getDiff(frame):
    image = frame.copy()
    bgSub = backgroundSubstraction(image)
    asd, diffImage = cv2.threshold(bgSub,10,255,cv2.THRESH_BINARY)

    return diffImage

def blackFilter(image, grayImage, value):
    hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    grayImage2 = grayImage.copy()
    mask = np.where(hsvImage[:,:,2] > value,0,255)

    hsvImage[:,:,2] = mask
    grayImage2[:] = np.where(mask > 120,255,0)

    return grayImage2

def rotateImage(image, degree):
    rotationMatrix = cv2.getRotationMatrix2D((Width/2,Height/2),degree, .6)
    rotatedImage = cv2.warpAffine(image, rotationMatrix, (Width, Height))

    return rotatedImage

def click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
