import cv2
import numpy as np
import collections

def getNotzeroPixels(image, groundMask, percentage = True):
    maskSize = cv2.countNonZero(groundMask)
    maskedImage = cv2.bitwise_and(image,image,mask = groundMask)
    nonZeroPixels = cv2.countNonZero(maskedImage)
    if percentage:
        return 100*nonZeroPixels/maskSize
    else:
        return nonZeroPixels

def getAverage(grayImage, groundMask):
    maskedImage = cv2.bitwise_and(grayImage, grayImage, mask = groundMask)
    average, dev = cv2.meanStdDev(maskedImage)
    imgSize = 1920*1080
    areaSize = cv2.countNonZero(groundMask)

    areaAverage = average * imgSize / areaSize

    return areaAverage[0][0]

def getAveragePixels(diffImage, grayImage, groundMask):
    nonZeroPixels = getNotzeroPixels(diffImage, groundMask, percentage = False)
    average = getAverage(grayImage, groundMask)
    if nonZeroPixels < 150:
        if getAveragePixels.count < 20:
            getAveragePixels.averageList.appendleft(average)
            getAveragePixels.average *= getAveragePixels.count
            getAveragePixels.average += int(average)
            getAveragePixels.average /= (getAveragePixels.count+1)
            getAveragePixels.count += 1
        elif getAveragePixels.average - average < 10 and average - getAveragePixels.average < 10:
            popped = getAveragePixels.averageList.pop()
            getAveragePixels.averageList.appendleft(int(average))
            getAveragePixels.average *= 20
            getAveragePixels.average -= popped
            getAveragePixels.average += int(average)
            getAveragePixels.average /= 20
    return getAveragePixels.average

getAveragePixels.count = 0
getAveragePixels.average = 0
getAveragePixels.averageList = collections.deque(20*[0],20)
