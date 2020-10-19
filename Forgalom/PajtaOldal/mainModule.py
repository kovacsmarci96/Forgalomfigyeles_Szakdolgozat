import cv2
import time

from imageProcessModule import *
from maskAreaModule import *
from carDetectModule import *
from carCountModule import*
from wayControllerModule import *
from databaseModule import *
from busDetectModule import *
from drawModule import *

Width = 1920
Height = 1080

source1 = 'BusLR.mp4'
source2 = 'BusLR_Night.mp4'
source3 = 'BusLR_Night2.mp4'
source4 = 'BusRL.mp4'
source5 = 'BusRL_Night.mp4'
source6 = 'BusRL_Night2.mp4'
source7 = 'PajtaOldal1.mp4'
source8 = 'PajtaOldal2.mp4'
source9 = 'PajtaOldal3.mp4'
source10 = 'PajtaOldal4.mp4'
source11 = 'PajtaOldal5.mp4'
source12 = 'PajtaOldalNight1.mp4'
source13 = 'PajtaOldalNight2.mp4'
source14 = 'PajtaOldalNight3.mp4'
PajtaOldal = A kamera RTSP cimet, jogi okokbol nem adhatom meg

def reset_attempts():
    return 50

def process_video(attempts):
    waysLR = []
    waysLRBikes = []
    complevelLR = (1100,1000)
    complevelLRNight = (1250,200)
    counterLR = 0
    counterLRBike = 0
    counterLRCars = 0
    counterLRVan = 0
    counterLRTruck = 0
    counterLRBus = 0

    waysRL = []
    complevelRL = (430,600)
    complevelRLNight = (750,300)
    counterRL = 0
    counterRLBike = 0
    counterRLCars = 0
    counterRLVan = 0
    counterRLTruck = 0
    counterRLBus = 0

    lastSecond = 00

    dayPart = 'Day'

    font = cv2.FONT_HERSHEY_SIMPLEX
    while(True):
        ret, frame = cap.read()
        now = datetime.datetime.now().time()
        
        if not ret:
            print("Disconnected at: %d:%d" % (now.hour, now.minute))
            cap.release()

            if attempts > 0:
                time.sleep(5)
                return True
            else:
                return False

        now = datetime.datetime.now().time()
        hour = now.hour
        minute = now.minute + now.hour * 60
        grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        if (minute < 1230 and minute > 330):
            dayPart = 'Day'
            
            filtered = filteringDay(frame)
            
            maskedLR = maskLRDay(filtered)
            matchesLR = detectVehicles(maskedLR,200,100)
            wayControllerLeft(matchesLR, waysLR, complevelLR, 300)
            counterLR, counterLRCars, counterLRBus, counterLRVan, counterLRTruck = counterLeft(waysLR, frame, grayFrame, counterLR, counterLRCars, counterLRBus, counterLRVan, counterLRTruck, complevelLR)

            maskedRL = maskRLDay(filtered)
            matchesRL = detectVehicles(maskedRL,200,100)
            wayControllerRight(matchesRL,waysRL,complevelRL,300)
            counterRL, counterRLCars, counterRLBus, counterRLVan, counterRLTruck = counterRight(waysRL, frame, grayFrame, counterRL, counterRLCars, counterRLBus, counterRLVan, counterRLTruck, complevelRL)
            
        else:
            dayPart = 'Night'
            
            filtered = filteringNight(frame)
            
            maskedLR = maskLRNight(filtered)
            matchesLR = detectVehicles(maskedLR,100,100)
            wayControllerLeft(matchesLR,waysLR, complevelLRNight, 300)
            counterLR, counterLRBus = counterLeftNight(waysLR, frame, grayFrame, counterLR, counterLRBus, complevelLRNight)

            maskedRL = maskRLNight(filtered)
            matchesRL = detectVehicles(maskedRL,200,100)
            wayControllerRight(matchesRL, waysRL, complevelRLNight, 300)
            counterRL, counterRLBus = counterRightNight(waysRL, frame, grayFrame, counterRL, counterRLBus, complevelRLNight)

        timer(waysLR)
        timeoutWays(waysLR,5)
        timer(waysRL)
        timeoutWays(waysRL,5)
        
        second = now.minute * 60 + now.second

        if(second % 600 == 0 and lastSecond != second):
            if(dayPart == 'Day'):
                saveToDB(counterLR, counterLRCars, counterLRVan, counterLRTruck, counterRL, counterRLCars, counterRLVan, counterRLTruck, dayPart)
                counterLR = 0
                counterLRCars = 0
                counterLRVan = 0
                counterLRTruck = 0
                counterLRBus = 0
                counterRL = 0
                counterRLCars = 0
                counterRLVan = 0
                counterRLTruck = 0
                counterRLBus = 0
                lastSecond = second
            else:
                saveToDBNight(counterLR, counterRL, dayPart)
                counterLR = 0
                counterLRCars = 0
                counterLRVan = 0
                counterLRTruck = 0
                counterLRBus = 0
                counterRL = 0
                counterRLCars = 0
                counterRLVan = 0
                counterRLTruck = 0
                counterRLBus = 0
                lastSecond = second
        
        statistics = np.zeros((Height,Width,3),np.uint8)
        stat = drawStatisticImage(statistics,counterLR, counterLRCars, counterLRVan, counterLRTruck, counterLRBus,
                                  counterRL, counterRLCars, counterRLVan, counterRLTruck, counterRLBus)


        image = cv2.resize(frame,(640,500))
        statistics = cv2.resize(stat,(640,500))

        cv2.moveWindow('image',0,0)
        cv2.moveWindow('stat',0,500)

        cv2.imshow('image',image)
        cv2.imshow('stat',statistics)
        
        k = cv2.waitKey(30)&0xFF
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()
            break


recall = True
attempts = reset_attempts()

while(recall):
    cap = cv2.VideoCapture(source1)
    now = datetime.datetime.now().time()

    if cap.isOpened():
        print("Camera connected at: %d:%d" % (now.hour, now.minute))
        attempts = reset_attempts()
        recall = process_video(attempts)
    else:
        print("Camera not opened at: %d:%d" % (now.hour, now.minute))
        cap.release()
        attempts -= 1
        print("attempts: " + str(attempts))

        time.sleep(5)
        continue

cap.release()
cv2.destroyAllWindows()
