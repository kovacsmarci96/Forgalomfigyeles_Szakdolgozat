import cv2
import numpy as np

Width = 1920
Height = 1080

def maskLRDay(frame):
    image = frame.copy()

    triangle = np.array([ [0,1000], [1530,370], [0,370] ], np.int32)
    cv2.fillConvexPoly(image, triangle,(0,255,0))

    triangle = np.array([ [1530,370], [1000,1080], [1920,1080] ], np.int32)
    cv2.fillConvexPoly(image, triangle,(0,255,0))

    cv2.rectangle(image,(0,0),(1920,370),(0,255,0),-1)
    cv2.rectangle(image,(0,730),(1920,1080),(0,255,0),-1)
    cv2.rectangle(image,(1530,0),(1920,1080),(0,255,0),-1)
    

    return image

def maskRLDay(frame):
    image = frame.copy()

    cv2.rectangle(image,(0,800),(Width,Height),(0,255,0),-1)
    cv2.rectangle(image,(960,0),(Width,Height),(0,255,0),-1)

    triangle = np.array([ [0,800], [Width,800], [Width,150] ], np.int32)
    cv2.fillConvexPoly(image, triangle,(0,255,0))

    triangle = np.array([ [0,600], [Width,0], [0,0] ], np.int32)
    cv2.fillConvexPoly(image, triangle,(0,255,0))

    return image

def maskLRNight(frame):
    image = frame.copy()

    cv2.rectangle(image,(0,0),(1920,400),(0,255,0),-1)
    
    triangle = np.array([ [0,0], [0,950], [2400,0] ], np.int32)
    cv2.fillConvexPoly(image, triangle,(0,255,0))

    return image

def maskRLNight(frame):
    image = frame.copy()

    cv2.rectangle(image,(0,950),(1920,1080),(0,255,0),-1)
    cv2.rectangle(image,(0,0),(1920,500),(0,255,0),-1)

    triangle = np.array([ [0,950], [1920,950], [1920,200] ], np.int32)
    cv2.fillConvexPoly(image, triangle,(0,255,0))


    return image

    

    
