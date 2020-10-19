import cv2
import numpy as np

from drawModule import *
from pixelCountModule import *
from parkingPlace import *

Width = 1920
Height = 1080

parkingLotUp = [(358, 370),(433, 369),(509, 365),(568, 357),(616, 358),(666, 359),(707, 355),(761, 351),(793, 352),(834, 351)]
parkingLotDown = [(370, 446),(424, 441),(474, 436),(526, 432),(578, 425),(614, 419),(660, 413),(704, 409),(752, 403),(795, 405),(836, 396),(851, 398),(899, 409),(950, 407),(974, 414),(1011, 416)]

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
percentages = int((1000-250)/10)*[0]
drawablePercentages = int((1000-250)/10)*[10]


currentX = 1000
while currentX > 250:
    rectangle = getRectangle(currentX, 70)
    mask = np.zeros((Height,Width), np.uint8)
    rect = np.array(rectangle, np.int32)
    cv2.fillConvexPoly(mask,rect,255)
    masks.append(mask)
    isRefreshable.append(False)
    currentX -= 10

def calculatePercentagesBack(processedImage, diffImage):
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

def setupDrawablePercentagesBack():
    percs = percentages[:]
    i = 1
    while i < len(percs)-1:
        drawablePercentages[i] = (percs[i-1] + percs[i] + percs[i+1]) / 3
        i += 1
        drawablePercentages[i] = percs[i]

def calculateStatusBack():
    parkingCars = []
    parkingCarsXPosition = []

    currentX = 1000
    lastPerc = 100
    increasing = False

    i = 0

    while currentX > 250:
        perc = drawablePercentages[i]

        if perc < lastPerc and increasing:
            increasing = False

            if lastPerc > 30:
                width = int(70)
                rectangle = getRectangle(currentX, width)

                parkingCars.append(parkingPlace(rectangle))
                parkingCarsXPosition.append(currentX)

        if perc > lastPerc:
            increasing = True

        lastPerc = perc
        currentX -= 10
        i += 1

    return parkingCars

def drawStatisticsOnImageBack(image):
    minY = 400
    maxY = 100
    scale = (minY-maxY)/100
    gridHeight = (minY-maxY)/5
    currX = 1620
    lastPercentage = drawablePercentages[0]


    for i in range(0,5):
        cv2.line(image,(1050,int(minY-i*gridHeight)),(1600, int(minY-i*gridHeight)),(255,255,255),3)
        if(i==0):
            space = ' '
        else:
            space= ''
            cv2.putText(image, space+str(i*20), (1000,int(minY-i*gridHeight+10)),1,2,(255,255,255),3)

    for i in range(0,5):
        cv2.line(image,(1050 + i*115,maxY),(1050+i*115,minY),(255,255,255),3)
    cv2.putText(image, space+str(1020), (1590, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(930), (1475, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(800), (1360, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(660), (1245, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(480), (1130, minY+40),1,2,(255,255,255),3)
    cv2.putText(image, space+str(330), (1015, minY+40),1,2,(255,255,255),3)
    

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

def drawOnRectanglesBack(image,start,diff):
    currX = 1000
    while currX > 250:
        rect = getRectangle(currX,70)
        currX -= 10*diff
        drawRectangleOnImage(image,rect,(0,0,255))

                            
