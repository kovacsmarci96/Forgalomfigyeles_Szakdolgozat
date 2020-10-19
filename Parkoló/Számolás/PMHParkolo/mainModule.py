import cv2
import time

from maskAreaModule import *
from workingModule import *

Width = 1920
Height = 1080

source1 = 'PMHParkolo.mp4'
source2 = 'PMHParkolo2.mp4'
#source3 = A kamera RTSP cimet, jogi okokbol nem adhatom meg

groundMask = getGroundMask(Width, Height)

def reset_attempts():
    return 50

def process_video(attempts):
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
            
        processImage(frame, groundMask)

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
