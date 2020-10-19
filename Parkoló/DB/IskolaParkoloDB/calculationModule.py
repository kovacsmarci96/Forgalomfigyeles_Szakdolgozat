import cv2
import numpy as np

from drawModule import *
from pixelCountModule import *
from parkingPlace import *

Width = 1280
Height = 720

parkingLotDown = [(59, 282),(84, 287),(107, 283),(126, 284),(147, 283),(181, 283),(199, 282),(226, 282),(260, 282),(289, 279),(325, 279),(350, 280),(393, 277),(440, 277),(470, 276),(508, 273),(543, 273),(580, 272),(617, 268),(653, 269),(691, 269),(728, 267),(765, 267),(821, 267),(863, 267),(907, 267),(946, 267),(991, 270),(1011, 270),(1026, 270)]
parkingLotUp = [(88, 253),(103, 255),(121, 255),(133, 252),(147, 257),(172, 255),(194, 254),(221, 254),(246, 253),(280, 253),(311, 256),(324, 251),(354, 251),(390, 253),(407, 249),(444, 249),(474, 249),(508, 248),(556, 250),(604, 250),(644, 250),(679, 250),(732, 250),(769, 250),(828, 250),(877, 250),(896, 250),(934, 250),(970, 250),(1019, 250)]


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

percentages = int((1000-250)/10)*[0]
drawablePercentages = int((1000-250)/10)*[10]

def makeRectangles(width):
    masks = []
    isRefreshable = []

    currentX = 1000
    while currentX > 250:
        rectangle = getRectangle(currentX, width)
        mask = np.zeros((Height,Width), np.uint8)
        rect = np.array(rectangle, np.int32)
        cv2.fillConvexPoly(mask,rect,255)
        masks.append(mask)
        isRefreshable.append(False)
        currentX -= 10
    return masks, isRefreshable


def calculatePercentages(processedImage, diffImage, masks, isRefreshable):
    newPercentage = int((1000-250)*10)*[0]
    currentX = 1000
    i = 0

    while currentX > 250:
        perc = getNotzeroPixels(processedImage, groundMask = masks[i], percentage = True)
        percMoving = getNotzeroPixels(diffImage, groundMask = masks[i], percentage = True)
        newPercentage[i] = perc

        if percMoving < 5:
            isRefreshable[i] = True
        else:
            isRefreshable[i] = False

        currentX -= 10
        i += 1

    for i in range(0,int((1000-250)/10)):
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

def setupDrawablePercentages():
    percs = percentages[:]
    i = 1
    while i < len(percs)-1:
        drawablePercentages[i] = (percs[i-1] + percs[i] + percs[i+1]) / 3
        i += 1
        drawablePercentages[i] = percs[i]

def calculateStatus(width, percs):
    parkingCars = []

    currentX = 1000
    lastPerc = 100
    increasing = False

    i = 0

    while currentX > 250:
        perc = drawablePercentages[i]

        if perc < lastPerc and increasing:
            increasing = False

            if lastPerc > percs:
                width = int(width)
                rectangle = getRectangle(currentX, width)

                parkingCars.append(parkingPlace(rectangle))

        if perc > lastPerc:
            increasing = True

        lastPerc = perc
        currentX -= 10
        i += 1

    return parkingCars

def drawStatisticsOnImage(image):
    minY = 500
    maxY = 200
    scale = (minY-maxY)/100
    gridHeight = (minY-maxY)/5
    currX = 1100
    lastPercentage = drawablePercentages[0]


    for i in range(0,5):
        cv2.line(image,(200,int(minY-i*gridHeight)),(1100, int(minY-i*gridHeight)),(255,255,255),3)
        if(i==0):
            space = ' '
        else:
            space= ''
            cv2.putText(image, space+str(i*20), (150,int(minY-i*gridHeight+10)),1,2,(255,255,255),3)

    for i in range(0,6):
        cv2.line(image,(200 + i*150,maxY),(200+i*150,minY),(255,255,255),3)
        cv2.putText(image, space+str(1050-i*150), (1050-i*150, minY+40),1,2,(255,255,255),3)
    
    cv2.line(image,(200,maxY),(200,minY),(255,255,255),3)
    cv2.line(image,(190,maxY+20),(200,maxY),(255,255,255),3)
    cv2.line(image,(210,maxY+20),(200,maxY),(255,255,255),3)
    cv2.putText(image, '%', (170,maxY-20),1,2,(255,255,255),2)

    cv2.line(image,(200,minY),(1100,minY),(255,255,255),3)
    cv2.line(image,(1090,minY-10),(1100,minY),(255,255,255),3)
    cv2.line(image,(1090,minY+10),(1100,minY),(255,255,255),3)
    cv2.putText(image, 'X', (800,minY+70),1,2,(255,255,255),2)

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
            cv2.line(image,(int(currX+10),int(minY-lastPercentage*scale)), (int(currX), int(minY-percentage*scale)),color,2)
            lastPercentage = percentage
            currX -= 10
    pass

def drawOnRectangles(image,start,diff):
    currX = 1000
    while currX > 250:
        rect = getRectangle(currX, 30)
        currX -= 10*diff
        drawRectangleOnImage(image,rect,(0,0,255))
        
                
    
    
