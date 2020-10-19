import datetime
import cv2
import os
from databaseModule import *

filedir = os.path.dirname(os.path.realpath('__file__'))

def save_frame(frame, cntr,direction, width=640, height=480, fileDir=filedir):
    img = frame.copy()
    #resize for save memory
    frame = cv2.resize(frame, (width,height))
    filename = 'hits/%s_%d.jpg' % (direction,cntr)
    filename = os.path.join(fileDir, filename)
    cv2.imwrite(filename,frame)
    return
