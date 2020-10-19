import cv2
import datetime

from imageProcessModule import *
from maskAreaModule import *
from pixelCountModule import *
from drawModule import *
from calculationModuleSmall import *
from calculationModuleBig import *

Width = 1280
Height = 720

def processImage(frame,groundMask):

    statistics = np.zeros((Height,Width,3),np.uint8)
    stat = drawStatisticImage(statistics)

    grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    diffImage = getDiff(frame)
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
    drawStatisticsOnImageBig(stat)

    calculatePercentagesSmall(maskedSmall, diffImage)
    setupDrawablePercentagesSmall()
    carsSmall = calculateStatusSmall()
    drawStatisticsOnImageSmall(stat)

    all = len(carsBig) + len(carsSmall)

    print("Big:", len(carsBig))
    print("Small:", len(carsSmall))
    print("All:", all)

    image = cv2.resize(frame,(640,500))
    statistics = cv2.resize(stat, (640,500))
    filteredBig = cv2.resize(rotatedBig,(640,500))
    filteredSmall = cv2.resize(maskedSmall,(640,500))

    cv2.moveWindow('image',0,0)
    cv2.moveWindow('statistics',0,500)
    cv2.moveWindow('filteredBig',640,0)
    cv2.moveWindow('filteredSmall',640,500)

    cv2.imshow('image',image)
    cv2.imshow('statistics',statistics)
    cv2.imshow('filteredBig',filteredBig)
    cv2.imshow('filteredSmall', filteredSmall)
