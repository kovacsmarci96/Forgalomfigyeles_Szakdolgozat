import cv2
import datetime
import numpy as np
import os
import platform
import sys

from imageProcessModule import *
from calculationModule import *
from calculationModuleLeft import *
from maskAreaModule import *
from databaseModule import *


def processImage(frame, lastFrame, dayTime, groundMask, lastSecond):

    cntCars = 0
    now = datetime.datetime.now().time()
    second = now.minute * 60 + now.second
    hour = now.hour

    if (second % 30 == 0 and lastSecond != second):
        statistics = np.zeros((Height,Width,3),np.uint8)

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diffImage = getGrayDiff(frame, lastFrame)
        average = getAveragePixels(diffImage, grayImage, groundMask)


        if(hour >= 18 and hour < 19):
            numb1 = average * 0.9
            numb2 = average * 0.8
        elif(hour>=19 and hour < 20):
            numb1 = average * 0.9
            numb2 = average * 0.85
        elif(hour >= 17 and hour < 18):
            numb1 = average * 0.8
            numb2 = average * 0.8
        elif(hour >= 16 and hour < 17):
            numb1 = average * 0.95
            numb2 = average * 1
        elif(hour > 5 and hour < 16):
            numb1 = average * 0.7
            numb2 = average * 0.6
        else:
            numb1 = average * 0.75
            numb2 = average * 0.8

        if(hour >= 16 and hour < 19):
            widthRight = 50
            percRight = 20
            widthLeft = 5
            percLeft = 20
        elif(hour > 5 and hour < 16):
            widthRight = 50
            percRight = 15
            widthLeft = 5
            percLeft = 15
        else:
            widthRight = 40
            percRight = 15
            widthLeft = 10
            percLeft = 20


    	blackFilteredRight = blackFilter(frame, grayImage, numb1)
        blackFilteredLeft = blackFilter(frame,grayImage, numb2)

        maskedRight = maskingRight(blackFilteredRight)
        maskedLeft = maskingLeft(blackFilteredLeft)

        maskRight, isRefreshableRight = makeRectangles(widthRight)
        maskLeft, isRefreshableLeft = makeRectanglesLeft(widthLeft)

        calculatePercentages(maskedRight,diffImage,maskRight,isRefreshableRight)
        calculatePercentagesLeft(maskedLeft, diffImage, maskLeft, isRefreshableLeft)

        setupDrawablePercentages()
        setupDrawablePercentagesLeft()

        carsRight = calculateStatus(widthRight, percRight)
        carsLeft = calculateStatusLeft(widthLeft, percLeft)
        
        cntCars = len(carsRight) + len(carsLeft)

        print("Left:", len(carsLeft))
        print("Right:", len(carsRight))
        print("All:",cntCars)

        saveToDB(cntCars, dayTime)
        lastSecond = second

    image = cv2.resize(frame,(640,500))
    cv2.moveWindow('image',0,0)
    cv2.imshow('image',image)

    return lastSecond
