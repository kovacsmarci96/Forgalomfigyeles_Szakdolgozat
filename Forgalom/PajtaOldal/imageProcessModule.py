import cv2

def background_substraction(frame, fgbg = cv2.createBackgroundSubtractorMOG2()):
    mask = fgbg.apply(frame)
    return mask


def filteringDay(frame):
    image = frame.copy()
    bgSub = background_substraction(image)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8,8))
    ret, threshold = cv2.threshold(bgSub, 127,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    open = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)
    dilate = cv2.dilate(close,kernel, iterations = 2)

    return dilate



def filteringNight(frame):
    image = frame.copy()
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))

    ret, threshold = cv2.threshold(grayImage, 0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    open = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)
    
    dilate = cv2.dilate(close, kernel)

    inv = cv2.bitwise_not(dilate)

    bgSub = background_substraction(dilate)

    return dilate

def click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
