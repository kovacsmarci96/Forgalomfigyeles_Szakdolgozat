import cv2
import time

from maskAreaModule import *
from workingModule import *

source1 = 'PMHDome.mp4'
source2 = 'PMHDome1.mp4'
source3 = 'PMHDome2.mp4'
source4 = 'PMHDome3.mp4'
#source5 = A kamera RTSP cimet, jogi okokbol nem adhatom meg

Width = 1280
Height = 720

cap = cv2.VideoCapture(source1)
ret,frame = cap.read()

lastFrame = frame.copy()

groundMask = getGroundMask(Width, Height)
dayPart = 'Day'

def reset_attempts():
    return 50

def process_video(attempts):
    lastSecond = 00
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
            
        hour = now.hour

        if (hour < 20 and hour > 5):
            dayPart = 'Day'
        else:
            dayPart = 'Night'
            
        lastFrame = frame.copy()
        lastSecond = processImage(frame, lastFrame, dayPart, groundMask, lastSecond)
        
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
