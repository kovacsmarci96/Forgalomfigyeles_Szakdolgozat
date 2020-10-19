import cv2

def getCenter(x, y, width, height):
    x1 = int(width/2)
    y1 = int(height/2)

    cx = x+x1
    cy = y+y1

    return (cx,cy)

def detectVehicles(mask, minContourWidth, minContourHeight):
    matches = []

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    for(i, contour) in enumerate(contours):
        (x,y,width,height) = cv2.boundingRect(contour)

        validContour = (width > minContourWidth) and (height > minContourHeight)

        if not validContour:
            continue

        center = getCenter(x,y,width,height)

        matches.append(((x,y,width,height),center))

    return matches
