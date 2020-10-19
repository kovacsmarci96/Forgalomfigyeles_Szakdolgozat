import cv2
import time
import datetime

from imageProcessModule import *
from carDetectModule import *
from carCountModule import *
from maskAreaModule import *
from wayControllerModule import *
from databaseModule import *
from drawModule import *

Width = 1280
Height = 720

source1 = 'SportCsarnok1.mp4'
source2 = 'SportCsarnok2.avi'
source3 = 'SportCsarnokNightRL1.mp4'
#source4 = A kamera RTSP cimet, jogi okokbol nem adhatom meg

def reset_attempts():
    return 50

def process_video(attempts):
    matches = []
    waysRL = []
    complevelRL = (500,343)
    complevelRLNight = (520,343)
    counterRL = 0

    waysLR = []
    complevelLR = (490,343)
    complevelLRNight = (520,343)
    counterLR = 0

    lastSecond = 00
    dayTime = 'Day'

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

        if (hour > 5 and hour < 20):
            masked = maskRoad(frame)
            filtered = filtering(masked)
                
            matches = detectVehicles(filtered,60,40)
            wayControllerRight(matches, waysRL, complevelRL,50)
            counterRL = counterRight(waysRL,frame,filtered,counterRL,complevelRL)

            wayControllerLeft(matches, waysLR, complevelLR,50)
            counterLR = counterLeft(waysLR,frame,filtered,counterLR,complevelLR)
        else:
            masked = maskRoadNight(frame)
            filtered = filteringNight(masked)

            matches = detectVehicles(filtered,60,20)
            wayControllerRight(matches, waysRL, complevelRLNight,40)
            counterRL = counterRight(waysRL,frame,filtered, counterRL,complevelRLNight)

            wayControllerLeft(matches, waysLR, complevelLR,40)
            counterLR = counterLeft(waysLR,frame,filtered ,counterLR,complevelLR)

        timer(waysRL)
        timeoutWays(waysRL,5)
        timer(waysLR)
        timeoutWays(waysLR,5)


        if(now.hour < 20 and now.hour > 5):
            dayTime = 'Day'
        else:
            dayTime = 'Night'
        second = now.minute * 60 + now.second

        if(second % 600 == 0 and lastSecond != second):
            saveToDB(counterLR,counterRL, dayTime)
            counterLR = 0
            counterRL = 0
            lastSecond = second

        frame = makeStatTable(frame, counterLR, counterRL)
        
        image = cv2.resize(frame,(640,500))
        cv2.moveWindow('image',0,0)
        cv2.imshow('image',image)

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


