import cv2

def drawRectangleOnImage(image,rect,color,width=3):
    cv2.line(image, rect[0],rect[1],color,width)
    cv2.line(image, rect[1],rect[2],color,width)
    cv2.line(image, rect[2],rect[3],color,width)
    cv2.line(image, rect[3],rect[0],color,width)

def drawStatisticImage(image):
    statistics = image.copy()
    cv2.line(statistics,(960,0),(960,1080),(255,255,255),3)
    cv2.line(statistics,(0,540),(1920,540),(255,255,255),3)
    cv2.putText(statistics, "Parkolo kozepe", (10,35),1,2,(255,255,255),3)
    cv2.putText(statistics, "Parkolo hatulja", (970,35),1,2,(255,255,255),3)
    cv2.putText(statistics, "Parkolo eleje", (970,575),1,2,(255,255,255),3)
    return statistics
