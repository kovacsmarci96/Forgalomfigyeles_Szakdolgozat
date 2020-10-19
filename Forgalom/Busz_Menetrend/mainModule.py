import time
from databaseModule import *
from datetime import datetime

RLCome = [252, 287, 312, 327, 342, 349, 357, 372, 377, 382, 387, 395, 402, 410, 417, 425, 432, 442, 449, 464, 479, 495, 509, 540, 569, 599, 607, 629, 659, 689, 719, 749, 779, 787, 809, 839, 847, 869, 907, 929, 958, 967, 989, 1019, 1027, 1049 ,1079, 1109, 1139, 1199, 1259, 1316, 1386]
LRCome = [44, 319, 379, 386, 414, 439, 457, 474, 504, 534, 564, 566, 594, 624, 652, 682, 712, 742, 769, 772, 802, 817, 829, 832, 847, 862, 877, 889, 892, 907, 924, 939, 949, 954, 969, 984, 999, 1009, 1014, 1029, 1044, 1059, 1069, 1074, 1089, 1104, 1119, 1129, 1139, 1144, 1159, 1189, 1219, 1249, 1279, 1334, 1399]

RLCome_weekend = [267, 297, 357, 417, 449, 479, 509, 539, 569, 599, 659, 719, 779, 839, 899, 929, 959, 989, 1019, 1049, 1079, 1109, 1139, 1199, 1259, 1316, 1386]
LRCome_weekend = [44, 89, 352, 392, 409, 474, 504, 534, 564, 594, 624, 652, 712, 772, 832, 892, 924, 954, 984, 1014, 1044, 1074, 1104, 1134, 1159, 1189, 1249, 1329, 1409]


dayPart = 'Day'
lastMinuteLeft = 0
lastMinuteRight = 0


while(True):
    now = (datetime.now().time())
    
    if (now.hour < 20 and now.hour > 5):
        dayPart = 'Day'
    else:
        dayPart = 'Night'

    today = datetime.today().strftime('%A')
    minutes = now.hour * 60 + now.minute

    if(today == 'Saturday' or today == 'Sunday'):
        for i in range (len(RLCome_weekend)):
            if (RLCome_weekend[i] == minutes and lastMinuteRight != minutes):
                saveToDBBusRight(2,dayPart)
                lastMinuteRight = RLCome_weekend[i]
                print('Pushed right weekend at: %d:%d') % (now.hour, now.minute)
        for i in range (len(LRCome_weekend)):
            if (LRCome_weekend[i] == minutes and lastMinuteLeft != minutes):
                saveToDBBusLeft(2,dayPart)
                lastMinuteLeft = LRCome_weekend[i]
                print('Pushed left weekend at: %d:%d') % (now.hour, now.minute)
    else:
        for i in range (len(RLCome)):
            if (RLCome[i] == minutes and lastMinuteRight != minutes):
                saveToDBBusRight(2,dayPart)
                lastMinuteRight = RLCome[i]
                print('Pushed right weekday at: %d:%d') % (now.hour, now.minute)
        for i in range (len(LRCome)):
            if (LRCome[i] == minutes and lastMinuteLeft != minutes):
                saveToDBBusLeft(2,dayPart)
                lastMinuteLeft = LRCome[i]
                print('Pushed left weekday at: %d:%d') % (now.hour, now.minute)
