import cv2
import numpy as np

from drawModule import *
from pixelCountModule import *
from parkingPlace import *

Width = 1920
Height = 1080

parkingLotUp = [(730, 551),(782, 543),(830, 529),(870, 525),(930, 514),(968, 508),(1017, 500),(1069, 494),(1122, 483),(1173, 472),(1214, 461),(1283, 452),(1329, 443),(1379, 430)]
parkingLotDown = [(731, 619),(777, 608),(828, 599),(870, 595),(928, 583),(993, 567),(1035, 562),(1084, 549),(1151, 537),(1195, 527),(1251, 522),(1294, 509),(1342, 503),(1381, 495)]


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
percentages = int((1300-650)/10)*[0]
drawablePercentages = int((1300-650)/10)*[10]


currentX = 1300
while currentX > 650:
    rectangle = getRectangle(currentX, 90)
    mask = np.zeros((Height,Width), np.uint8)
    rect = np.array(rectangle, np.int32)
    cv2.fillConvexPoly(mask,rect,255)
    masks.append(mask)
    isRefreshable.append(False)
    currentX -= 10

def calculatePercentagesMiddle(processedImage, diffImage):
    newPercentage = int((1300-650)*10)*[0]
    currentX = 1300
    i = 0

    while currentX > 650:
        perc = getNotzeroPixels(processedImage, groundMask = masks[i], percentage = True)
        percMoving = getNotzeroPixels(diffImage, groundMask = masks[i], percentage = True)
        newPercentage[i] = perc

        if percMoving < 5:
            isRefreshable[i] = True
        else:
            isRefreshable[i] = False

        currentX -= 10
        i += 1

    for i in range(0,int((1300-650)/10)):
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

def setupDrawablePercentagesMiddle():
    percs = percentages[:]
    i = 1
    while i < len(percs)-1:
        drawablePercentages[i] = (percs[i-1] + percs[i] + percs[i+1]) / 3
        i += 1
        drawablePercentages[i] = percs[i]

def calculateStatusMiddle():
    parkingCars = []

    currentX = 1300
    lastPerc = 100
    increasing = False

    i = 0

    while currentX > 650:
        perc = drawablePercentages[i]

        if perc < lastPerc and increasing:
            increasing = False

            if lastPerc > 15:
                width = int(90)
                rectangle = getRectangle(currentX, width)

                parkingCars.append(parkingPlace(rectangle))

        if perc > lastPerc:
            increasing = True

        lastPerc = perc
        currentX -= 10
        i += 1

    return parkingCars

def drawStatisticsOnImageMiddle(image):
    minY = 400
    maxY = 100
    scale = (minY-maxY)/100
    gridHeight = (minY-maxY)/5
    currX = 640
    lastPercentage = drawablePercentages[0]


    for i in range(0,5):
        cv2.line(image,(62,int(minY-i*gridHeight)),(640, int(minY-i*gridHeight)),(255,255,255),3)
        if(i==0):
            space = ' '
        else:
            space= ''
            cv2.putText(image, space+str(i*20), (12,int(minY-i*gridHeight+10)),1,2,(255,255,255),3)

    for i in range(0,4):
        cv2.line(image,(62 + i*125,maxY),(62+i*125,minY),(255,255,255),3)
    cv2.putText(image, space+str(1320), (560, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(1190), (405, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(1075), (280, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(900), (155, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(700), (30, minY+40),1,2,(255,255,255),3) 
    

    cv2.line(image,(62,maxY),(62,minY),(255,255,255),3)
    cv2.line(image,(52,maxY+20),(62,maxY),(255,255,255),3)
    cv2.line(image,(72,maxY+20),(62,maxY),(255,255,255),3)
    cv2.putText(image, '[%]', (62,maxY-20),1,2,(255,255,255),2)

    cv2.line(image,(62,minY),(590,minY),(255,255,255),3)
    cv2.line(image,(630,minY-10),(640,minY),(255,255,255),3)
    cv2.line(image,(630,minY+10),(640,minY),(255,255,255),3)
    cv2.putText(image, '[X]', (730,minY+40),1,2,(255,255,255),2)

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
