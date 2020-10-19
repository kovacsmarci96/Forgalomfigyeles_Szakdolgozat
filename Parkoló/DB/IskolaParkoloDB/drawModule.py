import cv2

def drawRectangleOnImage(image,rect,color,width=3):
    cv2.line(image, rect[0],rect[1],color,width)
    cv2.line(image, rect[1],rect[2],color,width)
    cv2.line(image, rect[2],rect[3],color,width)
    cv2.line(image, rect[3],rect[0],color,width)
