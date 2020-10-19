import cv2
import numpy as np

from drawModule import *
from pixelCountModule import *
from parkingPlace import *

Width = 1280
Height = 720

parkingLotUp = [(1153, 200), (1170, 204), (1192, 208), (1215, 214), (1234, 216)]
parkingLotDown = [(1172, 231), (1195, 233), (1213, 237), (1232, 240), (1243, 242)]


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
percentages = int(((1246-1166))/10)*[0]
drawablePercentages = int(((1246-1166)/10))*[10]


currentX = 1246
while currentX > 1166:
    rectangle = getRectangle(currentX, 50)
    mask = np.zeros((Height,Width), np.uint8)
    rect = np.array(rectangle, np.int32)
    cv2.fillConvexPoly(mask,rect,255)
    masks.append(mask)
    isRefreshable.append(False)
    currentX -= 10


def calculatePercentagesSmall(processedImage, diffImage):
    newPercentage = int(((1246-1166)*10))*[0]
    currentX = 1246
    i = 0

    while currentX > 1166:
        perc = getNotzeroPixels(processedImage, groundMask = masks[i], percentage = True)
        percMoving = getNotzeroPixels(diffImage, groundMask = masks[i], percentage = True)
        newPercentage[i] = perc

        if percMoving < 5:
            isRefreshable[i] = True
        else:
            isRefreshable[i] = False

        currentX -= 10
        i += 1

    for i in range(0,int((1246-1166)/10)):
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

def setupDrawablePercentagesSmall():
    percs = percentages[:]
    i = 1
    while i < len(percs)-1:
        drawablePercentages[i] = (percs[i-1] + percs[i] + percs[i+1]) / 3
        i += 1
        drawablePercentages[i] = percs[i]

def calculateStatusSmall():
    parkingCars = []

    currentX = 1246
    lastPerc = 100
    increasing = False

    i = 0

    while currentX > 1166:
        perc = drawablePercentages[i]

        if perc < lastPerc and increasing:
            increasing = False

            if lastPerc > 30:
                width = int(50)
                rectangle = getRectangle(currentX, width)

                parkingCars.append(parkingPlace(rectangle))

        if perc > lastPerc:
            increasing = True

        lastPerc = perc
        currentX -= 10
        i += 1

    return parkingCars

def drawStatisticsOnImageSmall(image):
    minY = 460
    maxY = 260
    scale = (minY-maxY)/100
    gridHeight = (minY-maxY)/5
    currX = 1140
    lastPercentage = drawablePercentages[0]

    for i in range(0,5):
        cv2.line(image,(760,int(minY-i*gridHeight)),(1160, int(minY-i*gridHeight)),(255,255,255),2)
        if(i==0):
            space = ' '
        else:
            space= ''
            cv2.putText(image, space+str(i*20), (710,int(minY-i*gridHeight+7)),1,2,(255,255,255),2)

    for i in range(0,1):
        cv2.putText(image, space+str(1233-i*117), (1160-i*117-20, minY+40),1,2,(255,255,255),2)

    

    cv2.line(image,(760,maxY),(760,minY),(255,255,255),3)
    cv2.line(image,(750,maxY+20),(760,maxY),(255,255,255),3)
    cv2.line(image,(770,maxY+20),(760,maxY),(255,255,255),3)
    cv2.putText(image, '%', (760,maxY-13),1,2,(255,255,255),2)

    cv2.line(image,(760,minY),(1160,minY),(255,255,255),3)
    cv2.line(image,(1150,minY-10),(1160,minY),(255,255,255),3)
    cv2.line(image,(1150,minY+10),(1160,minY),(255,255,255),3)
    cv2.putText(image, 'X', (1133,minY+70),1,2,(255,255,255),2)

    for i in range(len(drawablePercentages)):
        if i > 0:
            percentage = drawablePercentages[i]
            if lastPercentage < percentage:
                color = (255,0,0)
            elif lastPercentage > percentage:
                color = (0,0,255)
            else:
                color = (0,255,0)
            if (currX%120) == 0:
                color = (0,255,0)
            else:
                color = (0,0,255)
            cv2.line(image,(int(currX+60),int(minY-lastPercentage*scale)), (int(currX), int(minY-percentage*scale)),color,3)
            lastPercentage = percentage
            currX -= 60

def drawOnRectanglesSmall(image,start,diff):
    currX = 1246
    while currX > 1166:
        rect = getRectangle(currX, 60)
        currX -= 10*diff
        drawRectangleOnImage(image,rect,(0,0,255))

                            
