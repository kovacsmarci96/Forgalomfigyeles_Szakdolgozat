import cv2

def maskRoad(frame):
    image = frame.copy()

    cv2.rectangle(image,(0,0),(1280,347),(0,255,0),-1)
    cv2.rectangle(image,(0,428),(1280,720),(0,255,0),-1)
    cv2.rectangle(image,(600,0),(1280,720),(0,255,0),-1)
    cv2.rectangle(image,(0,0),(180,720),(0,255,0),-1)

    return image

def maskRoadNight(frame):
    image = frame.copy()

    cv2.rectangle(image,(0,0),(1280,380),(0,255,0),-1)
    cv2.rectangle(image,(0,450),(1280,720),(0,255,0),-1)
    cv2.rectangle(image,(600,0),(1280,720),(0,255,0),-1)
    cv2.rectangle(image,(0,0),(180,720),(0,255,0),-1)

    return image
