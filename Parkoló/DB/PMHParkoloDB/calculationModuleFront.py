import cv2
import numpy as np

from drawModule import *
from pixelCountModule import *
from parkingPlace import *

Width = 1920
Height = 1080

parkingLotDown = [(798, 812),(840, 823),(890, 839),(942, 856),(978, 853),(1026, 867),(1072, 877),(1124, 887),(1161, 894),(1219, 899),(1252, 915),(1280, 918),(1306, 923),(1341, 929),(1386, 939)]
parkingLotUp = [(799, 718),(846, 724),(898, 736),(936, 739),(974, 752),(1019, 760),(1050, 767),(1095, 778),(1131, 788),(1167, 795),(1214, 802),(1258, 812),(1290, 823),(1309, 824),(1330, 828)]

def getRectangle(currentX, width):

    glide = (-30*(1030-currentX)/(1030-60))/2

    i = 1
    while i < len(parkingLotUp) - 1 and parkingLotUp[i][0] < currentX - width/2 - glide:
        i += 1
        
    numb1 = float((parkingLotUp[i][0] - currentX + width/2 + glide)) / (parkingLotUp[i][0] - parkingLotUp[i-1][0])
    corn1 = (int(currentX - width/2 - glide), int(parkingLotUp[i][1] + (parkingLotUp[i-1][1] - parkingLotUp[i][1]) * numb1))

    while i < len(parkingLotUp)-1 and parkingLotUp[i][0] < currentX + width/2 - glide:
        i += 1

    numb4 = float((parkingLotUp[i][0] - currentX - width/2 + glide)) / (parkingLotUp[i][0] - parkingLotUp[i-1][0])
    corn4 = (int(currentX + width/2 - glide), int(parkingLotUp[i][1] + (parkingLotUp[i-1][1] - parkingLotUp[i][1]) * numb4))

    i = 1
    while i < len(parkingLotDown)-1 and parkingLotDown[i][0] < currentX - width/2 + glide:
        i += 1
    numb2 = float((parkingLotDown[i][0] - currentX + width/2 - glide)) / (parkingLotDown[i][0] - parkingLotDown[i-1][0])
    corn2 = (int(currentX - width/2 + glide), int(parkingLotDown[i][1] + (parkingLotDown[i-1][1] - parkingLotDown[i][1]) * numb2))

    while i < len(parkingLotDown)-1 and parkingLotDown[i][0] < currentX + width/2 + glide:
        i += 1
    numb3 = float((parkingLotDown[i][0] - currentX - width/2 - glide)) / (parkingLotDown[i][0] - parkingLotDown[i-1][0])
    corn3 = (int(currentX + width/2 + glide), int(parkingLotDown[i][1] + (parkingLotDown[i-1][1] - parkingLotDown[i][1]) * numb3))

    rectangle = (corn1,corn2,corn3,corn4)

    return rectangle

masks = []
isRefreshable = []
percentages = int((1400-800)/10)*[0]
drawablePercentages = int((1400-800)/10)*[10]


currentX = 1300
while currentX > 800:
    rectangle = getRectangle(currentX, 80)
    mask = np.zeros((Height,Width), np.uint8)
    rect = np.array(rectangle, np.int32)
    cv2.fillConvexPoly(mask,rect,255)
    masks.append(mask)
    isRefreshable.append(False)
    currentX -= 10

def calculatePercentagesFront(processedImage, diffImage):
    newPercentage = int((1300-800)*10)*[0]
    currentX = 1300
    i = 0

    while currentX > 800:
        perc = getNotzeroPixels(processedImage, groundMask = masks[i], percentage = True)
        percMoving = getNotzeroPixels(diffImage, groundMask = masks[i], percentage = True)
        newPercentage[i] = perc

        if percMoving < 5:
            isRefreshable[i] = True
        else:
            isRefreshable[i] = False

        currentX -= 10
        i += 1

    for i in range(0,int((1300-800)/10)):
        refresh = True
        if (i>0 and isRefreshable[i-1] == False):
            refresh = False
        if (i>1 and isRefreshable[i-2] == False):
            refresh = False
        if (i>2 and isRefreshable[i-3] == False):
            refresh = False
        if (i>3 and isRefreshable[i-4] == False):
            refresh = False

        if(i<len(isRefreshable)-1 and isRefreshable[i+1] == False):
            refresh = False
        if(i<len(isRefreshable)-2 and isRefreshable[i+2] == False):
            refresh = False
        if(i<len(isRefreshable)-3 and isRefreshable[i+3] == False):
            refresh = False
        if(i<len(isRefreshable)-4 and isRefreshable[i+4] == False):
            refresh = False

        if refresh:
            percentages[i] = newPercentage[i]
    pass

def setupDrawablePercentagesFront():
    percs = percentages[:]
    i = 1
    while i < len(percs)-1:
        drawablePercentages[i] = (percs[i-1] + percs[i] + percs[i+1]) / 3
        i += 1
        drawablePercentages[i] = percs[i]

def calculateStatusFront():
    parkingCars = []

    currentX = 1300
    lastPerc = 100
    increasing = False

    i = 0

    while currentX > 800:
        perc = drawablePercentages[i]

        if perc < lastPerc and increasing:
            increasing = False

            if lastPerc > 40:
                width = int(80)
                rectangle = getRectangle(currentX, width)

                parkingCars.append(parkingPlace(rectangle))

        if perc > lastPerc:
            increasing = True

        lastPerc = perc
        currentX -= 10
        i += 1

    return parkingCars

def drawStatisticsOnImageFront(image):
    minY = 940
    maxY = 640
    scale = (minY-maxY)/100
    gridHeight = (minY-maxY)/5
    currX = 1620
    lastPercentage = drawablePercentages[0]


    for i in range(0,5):
        cv2.line(image,(1050,int(minY-i*gridHeight)),(1620, int(minY-i*gridHeight)),(255,255,255),3)
        if(i==0):
            space = ' '
        else:
            space= ''
            cv2.putText(image, space+str(i*20), (1000,int(minY-i*gridHeight+10)),1,2,(255,255,255),3)

    for i in range(0,3):
        cv2.line(image,(1050 + i*183,maxY),(1050+i*183,minY),(255,255,255),3)
    cv2.putText(image, space+str(1740), (1587, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(1490), (1394, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(1210), (1201, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(840), (1050, minY+40),1,2,(255,255,255),3)

    

    cv2.line(image,(1050,maxY),(1050,minY),(255,255,255),3)
    cv2.line(image,(1040,maxY+20),(1050,maxY),(255,255,255),3)
    cv2.line(image,(1060,maxY+20),(1050,maxY),(255,255,255),3)
    cv2.putText(image, '[%]', (1070,maxY-20),1,2,(255,255,255),2)

    cv2.line(image,(1050,minY),(1620,minY),(255,255,255),3)
    cv2.line(image,(1615,minY-10),(1620,minY),(255,255,255),3)
    cv2.line(image,(1615,minY+10),(1620,minY),(255,255,255),3)
    cv2.putText(image, '[X]', (1700,minY+40),1,2,(255,255,255),2)

    for i in range(len(drawablePercentages)):
        if i > 0:
            percentage = drawablePercentages[i]
            if lastPercentage < percentage:
                color = (255,0,0)
            elif lastPercentage > percentage:
                color = (0,0,255)
            else:
                color = (0,255,0)
            if (currX%20) == 0:
                color = (0,255,0)
            else:
                color = (0,0,255)
            cv2.line(image,(int(currX+10),int(minY-lastPercentage*scale)), (int(currX), int(minY-percentage*scale)),color,3)
            lastPercentage = percentage
            currX -= 10

    pass
