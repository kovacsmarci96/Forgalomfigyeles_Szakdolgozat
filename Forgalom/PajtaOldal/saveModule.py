import datetime
import cv2
import os
from databaseModule import *

filedir = os.path.dirname(os.path.realpath('__file__'))

def save_frame(frame, cntr,direction, width=640, hight=480, fileDir=filedir):
    img = frame.copy()
    #resize for save memory
    frame = cv2.resize(frame, (width,hight))
    filename = 'hits/%s_%d.jpg' % (direction,cntr)
    filename = os.path.join(fileDir, filename)
    cv2.imwrite(filename,frame)
    return

def save_frame_bus(frame,dir, counter, width=1920, hight=1080, fileDir=filedir):
    img = frame.copy()
    #resize for save memory
    frame = cv2.resize(frame, (width,hight))
    filename = 'buses_hits/bus_%s_%d.jpg' % (dir,counter)
    filename = os.path.join(fileDir, filename)
    cv2.imwrite(filename,frame)
    return
