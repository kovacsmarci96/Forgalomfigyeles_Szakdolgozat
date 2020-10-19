from saveModule import *

def counterLeft(ways, frame, filtered, counter, complevel):
    for i,way in enumerate(ways):
        if way.endP[0] > complevel[0]:
            counter += 1
            save_frame(frame,counter,"Left")
            ways.remove(way)
    return counter

def counterRight(ways,frame, filtered,counter,complevel):
    for i, way in enumerate(ways):
        if way.endP[0] < complevel[0]:
            counter+=1
            save_frame(frame,counter,"Right")
            ways.remove(way)
    return counter
