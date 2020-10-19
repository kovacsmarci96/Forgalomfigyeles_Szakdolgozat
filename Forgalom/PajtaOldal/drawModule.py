import cv2

Width = 1920
Height = 1080

font = cv2.FONT_HERSHEY_SIMPLEX

def drawStatisticImage(frame, counterLROut, counterLRCars, counterLRVan, counterLRTruck, counterLRBus,
                       counterRLOut, counterRLCars, counterRLVan, counterRLTruck, counterRLBus):
    stats = frame.copy()

    cv2.line(stats,(640,0),(640,1080),(255,255,255),3)
    cv2.line(stats,(1280,0),(1280,1080),(255,255,255),3)

    cv2.line(stats,(0,180),(1920,180),(255,255,255),3)
    cv2.line(stats,(0,360),(1920,360),(255,255,255),3)
    cv2.line(stats,(0,540),(1920,540),(255,255,255),3)
    cv2.line(stats,(0,720),(1920,720),(255,255,255),3)
    cv2.line(stats,(0,900),(1920,900),(255,255,255),3)

    cv2.putText(stats,'LR',(930,90), font, 2,(0,0,255),3,cv2.LINE_AA)
    cv2.putText(stats,'RL',(1570,90), font, 2,(0,255,0),3,cv2.LINE_AA)

    cv2.putText(stats,'Car',(270,270), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'Van',(270,450), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'Truck',(240,630), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'Bus',(270,810), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'All',(290,990), font, 2,(255,255,0),3,cv2.LINE_AA)

    cv2.putText(stats,'%d' % counterLRCars,(930,270), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterLRVan,(930,450), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterLRTruck,(930,630), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterLRBus,(930,810), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterLROut,(930,990), font, 2,(255,255,0),3,cv2.LINE_AA)

    cv2.putText(stats,'%d' % counterRLCars,(1570,270), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterRLVan,(1570,450), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterRLTruck,(1570,630), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterRLBus,(1570,810), font, 2,(255,255,0),3,cv2.LINE_AA)
    cv2.putText(stats,'%d' % counterRLOut,(1570,990), font, 2,(255,255,0),3,cv2.LINE_AA)
  
    return stats

    

