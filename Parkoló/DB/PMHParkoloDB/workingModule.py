import cv2
import numpy as np
import datetime

from imageProcessModule import *
from maskAreaModule import *
from pixelCountModule import *
from calculationModuleBack import *
from calculationModuleMiddle import *
from calculationModuleFront import *
from databaseModule import *

Width = 1920
Height = 1080

def processImage(frame, lastFrame, groundMask, lastSecond):
    cntMiddle = 0
    cntBack = 0
    cntFront = 0
    cntAll = 0

    now = datetime.datetime.now().time()
    second = now.minute * 60 + now.second

    if(second % 30 == 0 and lastSecond != second):

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diffImage = getGrayDiff(frame, lastFrame)
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
        maskedBack = maskBack(blackFilteredBack)
        maskedMiddle = maskMiddle(blackFilteredMiddle)

        rotatedFront = rotateImage(blackFilteredFront, -30)

        calculatePercentagesMiddle(maskedMiddle, diffImage)
        setupDrawablePercentagesMiddle()
        carsMiddle = calculateStatusMiddle()
        cntMiddle = len(carsMiddle)

        calculatePercentagesFront(rotatedFront, diffImage)
        setupDrawablePercentagesFront()
        carsFront = calculateStatusFront()
        cntFront = len(carsFront)

        calculatePercentagesBack(maskedBack, diffImage)
        setupDrawablePercentagesBack()
        carsBack = calculateStatusBack()
        cntBack = len(carsBack)

        cntAll = cntMiddle + cntFront + cntBack

        print("Front:",cntFront)
        print("Middle:",cntMiddle)
        print("Back:",cntBack)
        print("All:",cntAll)

        saveToDB(cntMiddle, cntFront, cntBack, cntAll)
        lastSecond = second

    image = cv2.resize(frame,(640,500))
    cv2.moveWindow('image',0,0)
    cv2.imshow('image',image)

    return lastSecond
