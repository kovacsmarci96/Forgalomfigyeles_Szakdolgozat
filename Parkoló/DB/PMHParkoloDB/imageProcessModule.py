import cv2
import numpy as np

Width = 1920
Height = 1080

def getGrayDiff(image, lastImage):
    diff1 = cv2.addWeighted(image,1,lastImage,-1,0)
    diff2 = cv2.addWeighted(lastImage,1,image,-1,0)
    diff = cv2.add(diff1,diff2)
    grayDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayDiff,10,255,cv2.THRESH_BINARY)

    return thresh

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
