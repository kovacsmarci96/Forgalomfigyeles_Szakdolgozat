import cv2
import numpy as np
import datetime

from imageProcessModule import *
from maskAreaModule import *
from pixelCountModule import *
from drawModule import *
from calculationModuleSmall import *
from calculationModuleBig import *
from databaseModule import *

Width = 1280
Height = 720

def processImage(frame, lastFrame, dayPart, groundMask, lastSecond):
    cntBig = 0
    cntSmall = 0
    cntAll = 0

    now = datetime.datetime.now().time()
    second = now.minute * 60 + now.second

    if(second % 30 == 0 and lastSecond != second):

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diffImage = getGrayDiff(frame, lastFrame)
        average = getAveragePixels(diffImage, grayImage, groundMask)

        hour = (datetime.datetime.now().time()).hour

        if (hour < 14 and hour > 5):
            numb1 = average * 0.8
            numb2 = average * 0.1
        elif (hour > 13 and hour < 18):
            numb1 = average * 0.5
            numb2 = average * 0.1
        elif (hour > 17 and hour < 20):
            numb1 = average * 0.6
            numb2 = average * 0.3
        else:
            numb1 = average * 0.65
            numb2 = average * 0.6

        if hour < 14 and hour > 5:
            percsBig = 30
            sizeBig = 60
        elif hour < 18 and hour > 13:
            percsBig = 30
            sizeBig = 45
        else:
            percsBig = 50
            sizeBig = 60

        blackFilteredBig = blackFilter(frame, grayImage, numb1)
        blackFilteredSmall = blackFilter(frame, grayImage, numb2)

        maskedBig = maskBig(blackFilteredBig)
	rotatedBig = rotateImage(maskedBig, 290)

	maskedSmall = maskSmall(blackFilteredSmall)

	masks, isRefreshable = makeRectanglesBig(sizeBig)

        calculatePercentagesBig(rotatedBig, diffImage, masks, isRefreshable)
        setupDrawablePercentagesBig()
        carsBig = calculateStatusBig(percsBig, sizeBig)
        cntBig = len(carsBig)

        calculatePercentagesSmall(maskedSmall, diffImage)
        setupDrawablePercentagesSmall()
        carsSmall = calculateStatusSmall()
        cntSmall = len(carsSmall)

        cntAll = cntBig + cntSmall
        print("Big:", cntBig)
        print("Small:", cntSmall)
        print("All:", cntAll)

        saveToDB(cntBig, cntSmall, cntAll, dayPart)
        lastSecond = second
    
    image = cv2.resize(frame,(640,500))
    cv2.moveWindow('image',640,0)
            
    cv2.imshow('image',image)

    return lastSecond
