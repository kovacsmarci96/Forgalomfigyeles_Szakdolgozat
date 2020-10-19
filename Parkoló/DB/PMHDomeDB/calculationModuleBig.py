import cv2
import numpy as np
import datetime

from drawModule import *
from pixelCountModule import *
from parkingPlace import *

Width = 1280
Height = 720

parkingLotDown = [(495, 303), (522, 313), (543, 313), (567, 320), (591, 326), (602, 330), (621, 332), (648, 340), (666, 344), (687, 347), (711, 353), (732, 356), (761, 364), (777, 370), (795, 373), (812, 379)]
parkingLotUp = [(487, 366), (510, 378), (542, 388), (566, 390), (598, 397), (629, 406), (654, 408), (672, 411), (701, 408), (726, 410), (746, 410), (760, 414), (777, 417), (798, 422), (812, 423), (823, 426)]


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


percentages = int((900-450)/10)*[0]
drawablePercentages = int((900-450)/10)*[10]

def makeRectanglesBig(size):
    masks = []
    isRefreshable = []
    currentX = 900
    while currentX > 450:
        rectangle = getRectangle(currentX, size)
        mask = np.zeros((Height,Width), np.uint8)
        rect = np.array(rectangle, np.int32)
        cv2.fillConvexPoly(mask,rect,255)
        masks.append(mask)
        isRefreshable.append(False)
        currentX -= 10
    return masks, isRefreshable
    

def calculatePercentagesBig(processedImage, diffImage, masks, isRefreshable):
    newPercentage = int((900-450)*10)*[0]
    currentX = 900
    i = 0

    while currentX > 467:
        perc = getNotzeroPixels(processedImage, groundMask = masks[i], percentage = True)
        percMoving = getNotzeroPixels(diffImage, groundMask = masks[i], percentage = True)
        newPercentage[i] = perc

        if percMoving < 5:
            isRefreshable[i] = True
        else:
            isRefreshable[i] = False

        currentX -= 10
        i += 1

    for i in range(0,int((900-450)/10)):
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

def setupDrawablePercentagesBig():
    percs = percentages[:]
    i = 1
    while i < len(percs)-1:
        drawablePercentages[i] = (percs[i-1] + percs[i] + percs[i+1]) / 3
        i += 1
        drawablePercentages[i] = percs[i]

def calculateStatusBig(percs, size):
    parkingCars = []

    currentX = 900
    lastPerc = 100
    increasing = False

    i = 0

    while currentX > 450:
        perc = drawablePercentages[i]

        if perc < lastPerc and increasing:
            increasing = False

            if lastPerc > percs:
                width = int(size)
                rectangle = getRectangle(currentX, width)

                parkingCars.append(parkingPlace(rectangle))

        if perc > lastPerc:
            increasing = True

        lastPerc = perc
        currentX -= 10
        i += 1

    return parkingCars

def drawStatisticsOnImageBig(image):
    minY = 460
    maxY = 260
    scale = (minY-maxY)/100
    gridHeight = (minY-maxY)/5
    currX = 550
    lastPercentage = drawablePercentages[0]


    for i in range(0,5):
        cv2.line(image,(153,int(minY-i*gridHeight)),(553, int(minY-i*gridHeight)),(255,255,255),3)
        if(i==0):
            space = ' '
        else:
            space= ''
            cv2.putText(image, space+str(i*20), (100,int(minY-i*gridHeight+10)),1,2,(255,255,255),3)

    for i in range(0,5):
        cv2.line(image,(153 + i*83,maxY),(153+i*83,minY),(255,255,255),2)
    cv2.putText(image, space+str(833), (553, minY+40),1,2,(255,255,255),2)
    cv2.putText(image, space+str(813), (450, minY+40),1,2,(255,255,255),2)
    cv2.putText(image, space+str(780), (366, minY+40),1,2,(255,255,255),2)
    cv2.putText(image, space+str(706), (283, minY+40),1,2,(255,255,255),2)
    cv2.putText(image, space+str(620), (200, minY+40),1,2,(255,255,255),2)
    cv2.putText(image, space+str(473), (116, minY+40),1,2,(255,255,255),2)

    

    cv2.line(image,(153,maxY),(153,minY),(255,255,255),3)
    cv2.line(image,(143,maxY+20),(153,maxY),(255,255,255),3)
    cv2.line(image,(163,maxY+20),(153,maxY),(255,255,255),3)
    cv2.putText(image, '%', (153,maxY-20),1,2,(255,255,255),2)

    cv2.line(image,(153,minY),(553,minY),(255,255,255),3)
    cv2.line(image,(543,minY-10),(553,minY),(255,255,255),3)
    cv2.line(image,(543,minY+10),(553,minY),(255,255,255),3)
    cv2.putText(image, 'X', (533,minY+70),1,2,(255,255,255),2)

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

def drawOnRectanglesBig(image,start,diff):
    currX = 800
    while currX > 450:
        rect = getRectangle(currX, 60)
        currX -= 10*diff
        drawRectangleOnImage(image,rect,(0,0,255))

                            
