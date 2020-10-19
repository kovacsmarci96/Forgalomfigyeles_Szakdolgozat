import cv2

def background_substraction(frame, fgbg = cv2.createBackgroundSubtractorMOG2(5000,5,True)):
    mask = fgbg.apply(frame)
    return mask

def filter(frame):
    image = frame.copy()

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12,12))

    ret, threshold = cv2.threshold(image, 127,255, cv2.THRESH_BINARY)

    open = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    close = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel)

    dilate = cv2.dilate(close,kernel)

    return dilate

def filtering(frame):
    bgSub = background_substraction(frame)
    filtered = filter(bgSub)

    return filtered

def click_event(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)

def filteringNight(frame):
    image = frame.copy()

    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))

    ret, threshold = cv2.threshold(grayImage,127,255, cv2.THRESH_BINARY)

    open = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

    inv = cv2.bitwise_not(open)
    return inv
