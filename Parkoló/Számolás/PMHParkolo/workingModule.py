import cv2
import numpy as np
import datetime

from imageProcessModule import *
from maskAreaModule import *
from pixelCountModule import *
from calculationModuleBack import *
from calculationModuleMiddle import *
from calculationModuleFront import *

Width = 1920
Height = 1080

def processImage(frame, groundMask):
    statistics = np.zeros((Height,Width,3),np.uint8)
    statistics = drawStatisticImage(statistics)

    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diffImage = getDiff(frame)
    average = getAveragePixels(diffImage, grayImage, groundMask)

    now = (datetime.datetime.now().time()).hour

    if (now < 15) and (now > 5):
        numb1 = average * 0.3
        numb2 = average * 0.2
        numb3 = average * 0.25
    elif (now > 14) and (now < 18):
        numb1 = average * 0.6
        numb2 = average * 0.05
        numb3 = average * 0.3
    elif(now > 17) and (now < 19):
        numb1 = average * 0.6
        numb2 = average * 0.04
        numb3 = average * 0.2
    else:
        numb1 = average * 0.3
        numb2 = average * 0.4
        numb3 = average * 0.2

    blackFilteredMiddle = blackFilter(frame, grayImage, numb1)
    blackFilteredFront = blackFilter(frame, grayImage, numb2)
    blackFilteredBack = blackFilter(frame, grayImage, numb3)

    maskedFront = maskFront(blackFilteredFront)
    maskedMiddle = maskMiddle(blackFilteredMiddle)
    maskedBack = maskBack(blackFilteredBack)

    rotatedFront = rotateImage(maskedFront, -30)

    calculatePercentagesMiddle(maskedMiddle, diffImage)
    setupDrawablePercentagesMiddle()
    carsMiddle = calculateStatusMiddle()
    drawStatisticsOnImageMiddle(statistics)

    calculatePercentagesFront(rotatedFront, diffImage)
    setupDrawablePercentagesFront()
    carsFront = calculateStatusFront()
    drawStatisticsOnImageFront(statistics)

    calculatePercentagesBack(maskedBack, diffImage)
    setupDrawablePercentagesBack()
    carsBack = calculateStatusBack()
    drawStatisticsOnImageBack(statistics)

    all = len(carsFront) + len(carsMiddle) + len(carsBack)

    print("Front:",len(carsFront))
    print("Middle:",len(carsMiddle))
    print("Back:",len(carsBack))
    print("All:",all)

    image = cv2.resize(frame,(640,500))
    stat = cv2.resize(statistics,(640,500))
    filteredFront = cv2.resize(rotatedFront,(640,500))
    filteredMiddle = cv2.resize(maskedMiddle,(640,500))
    filteredBack = cv2.resize(maskedBack,(640,500))

    cv2.moveWindow('image',0,0)
    cv2.moveWindow('stat',0,500)
    cv2.moveWindow('filteredFront',640,0)
    cv2.moveWindow('filteredMiddle',640,500)
    cv2.moveWindow('filteredBack',1280,0)


    cv2.imshow('image',image)
    cv2.imshow('stat',stat)
    cv2.imshow('filteredFront', filteredFront)
    cv2.imshow('filteredMiddle', filteredMiddle)
    cv2.imshow('filteredBack',filteredBack)
