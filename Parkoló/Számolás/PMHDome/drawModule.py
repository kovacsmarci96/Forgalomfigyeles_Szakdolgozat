import cv2

def drawRectangleOnImage(image,rect,color,width=3):
    cv2.line(image, rect[0],rect[1],color,width)
    cv2.line(image, rect[1],rect[2],color,width)
    cv2.line(image, rect[2],rect[3],color,width)
    cv2.line(image, rect[3],rect[0],color,width)


def drawStatisticImage(image):
    statistics = image.copy()
    cv2.line(statistics,(640,0),(640,720),(255,255,255),3)
    cv2.putText(statistics, "Parkolo bal", (7,23),1,2,(255,255,255),3)
    cv2.putText(statistics, "Parkolo jobb", (647,35),1,2,(255,255,255),3)
    return statistics
