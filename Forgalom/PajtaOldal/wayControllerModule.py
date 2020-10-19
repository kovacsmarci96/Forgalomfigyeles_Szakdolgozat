from wayModule import *

def wayControllerLeft(matches, ways, complevel, mindist):
    if len(matches) != 0:
        if((len(ways) == 0) & (matches[0][1] < complevel)):
            ways.append(Way(matches[0][1]))

        else:
            for i, way in enumerate(ways):
                for(j, match) in enumerate(matches):
                    #print(abs(way.endP[0] - match[1][0]))
                    if((abs(way.endP[0] - match[1][0]) < mindist) & (match[1][0] > way.endP[0])):
                       way.setEndP(match[1])
                       way.setLength(match[0][2])
                       way.setSize(match[0][3])
    return

def wayControllerRight(matches, ways, complevel, mindist):
    if len(matches) != 0:
        if((len(ways) == 0) & (matches[0][1] > complevel)):
            ways.append(Way(matches[0][1]))

        else:
            for i, way in enumerate(ways):
                for(j, match) in enumerate(matches):
                    if((abs(way.endP[0] - match[1][0]) < mindist) & (match[1][0] < way.endP[0])):
                        way.setEndP(match[1])
                        way.setLength(match[0][2])
                        way.setSize(match[0][3])


    return

def timer(ways):
    for i,way in enumerate(ways):
        way.Timer()
    return


def timeoutWays(ways, timermax):
    for i,way in enumerate(ways):
        if way.timer > timermax:
            ways.remove(way)
            return
