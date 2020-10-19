import cv2

def makeStatTable(frame, counterLR, counterRL):
    image = frame.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.line(image,(300,600),(600,600),(0,0,0),5)
    cv2.line(image,(300,450),(600,450),(0,0,0),5)

    cv2.line(image,(300,450),(300,600),(0,0,0),5)
    cv2.line(image,(600,450),(600,600),(0,0,0),5)

    cv2.line(image,(300,525),(600,525),(0,0,0),5)
    cv2.line(image,(450,450),(450,600),(0,0,0),5)

    cv2.putText(image,'Balrol',(330,500), font, 1,(0,0,255),2,cv2.LINE_AA)
    cv2.putText(image,'Jobbrol',(320,570), font, 1,(0,255,0),2,cv2.LINE_AA)

    cv2.putText(image,'%d' % counterLR,(510,500), font, 1,(0,0,255),2,cv2.LINE_AA)
    cv2.putText(image,'%d' % counterRL,(510,570), font, 1,(0,255,0),2,cv2.LINE_AA)

    return image
    
