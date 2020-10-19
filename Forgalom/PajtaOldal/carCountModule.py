from saveModule import *
from busDetectModule import *

def countVans(width, height, direction):
    if (direction == 'Left'):
        if(width < 590 and width > 375 and height < 315 and height > 245):
            return True
    else:
        if(height > 230 and height < 380 and width < 660 and width > 420):
            return True

def countCars(width, height, direction):
    if(direction == 'Left'):
        if(width < 550 and width > 210 and height < 300 and height > 150):
            return True
    else:
        if(width < 560 and width > 200 and height < 285 and height > 80):
            return True

def countBig(width,height,direction):
    if(direction == 'Left'):
        if(width < 800 and width > 400 and height < 400 and height > 300):
            return True
    else:
        if(width < 800 and width > 600 and height < 500 and height > 300):
            return True

        
def countBusNight(width, height, direction):
    if(direction == 'Left'):
        if(width > 500 and width < 1300 and height > 280 and height < 700):
            return True
    else:
        if(width > 300 and width < 1000 and height > 100 and height < 400):
            return True

def counterLeft(ways, frame, grayFrame, counter, counterCars, counterBus, counterVan, counterTruck, complevel):

    countCar = True
    countVan = True
    counterBusDB = 0

    for i,way in enumerate(ways):
        if way.endP[0] > complevel[0]:
            counter += 1
            if(countBig(way.length, way.size, 'Left') == True):
                if(detectBus(grayFrame,templateBusesLR,0.6) == True):
                    counterBus += 1
                    counterBusDB += 1
                    saveToDBBusLeft(counterBusDB, 'Day')
                    counterBusDB = 0
                    save_frame_bus(frame,'Left', counter)
                else:
                    counterTruck += 1
                    countVan = False
            if(countVans(way.length, way.size, 'Left') == True and countVan == True):
                counterVan += 1
                countCar = False
            if(countCars(way.length, way.size, 'Left') == True and countCar == True):
                counterCars += 1
            ways.remove(way)
    return counter, counterCars, counterBus, counterVan, counterTruck

def counterLeftNight(ways, frame, grayFrame, counter, counterBus, complevel):

    counterBusDB = 0
    
    for i,way in enumerate(ways):
        if way.endP[0] > complevel[0]:
            counter += 1
            if(countBusNight(way.length, way.size, 'Left') == True):
                if(detectBus(grayFrame, templateBusesLRNight,0.6) == True):
                    counterBus += 1
                    counterBusDB += 1
                    saveToDBBusLeft(counterBusDB, 'Night')
                    counterBusDB = 0
                    save_frame_bus(frame,'Left_Night', counter)
            print('Szeles:', way.length)
            print('Magas:', way.size)
            ways.remove(way)
    return counter, counterBus

def counterRight(ways, frame, grayFrame, counter, counterCars, counterBus, counterVan, counterTruck, complevel):
    
    countVan = True
    countCar = True
    counterBusDB = 0

    for i, way in enumerate(ways):
        if way.endP[0] < complevel[0]:
            counter+=1
            print('Szeles:', way.length)
            print('Magas:', way.size)
            if(countBig(way.length, way.size, 'Right') == True):
                if(detectBus(grayFrame,templateBusesRL,0.6) == True):
                    counterBus += 1
                    counterBusDB += 1
                    saveToDBBusRight(counterBusDB, 'Day')
                    counterBusDB = 0
                    save_frame_bus(frame,'Right', counter)
                else:
                    counterTruck += 1
                countVan = False
            if(countVans(way.length, way.size, 'Right') == True and countVan == True):
                if(detectBus(grayFrame,templateBusesRL,0.6) == True):
                    counterBus += 1
                    counterBusDB += 1
                    saveToDBBusRight(counterBusDB, 'Day')
                    counterBusDB = 0
                    save_frame_bus(frame,'Right', counter)
                else:
                    counterVan +=1
                    countCar = False
            if(countCars(way.length, way.size, 'Right') == True and countCar == True):
                counterCars += 1
            ways.remove(way)
    return counter, counterCars, counterBus,counterVan, counterTruck


def counterRightNight(ways, frame, grayFrame, counter, counterBus, complevel):

    counterBusDB = 0

    for i, way in enumerate(ways):
        if way.endP[0] < complevel[0]:
            if(countBusNight(way.length, way.size, 'Right') == True):
                if(detectBus(grayFrame, templateBusesRLNight,0.8) == True):
                    counterBus += 1
                    counterBusDB += 1
                    saveToDBBusRight(counterBusDB, 'Night')
                    counterBusDB = 0
                    save_frame_bus(frame,'Right_night', counter)
            print('Szeles:', way.length)
            print('Magas:', way.size)
            counter+=1
            ways.remove(way)
    return counter, counterBus
