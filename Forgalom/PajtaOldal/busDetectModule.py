import cv2
import numpy as np

bus_LR1 = cv2.imread('buses/bus1_1.jpg',0)
bus_LR2 = cv2.imread('buses/bus1_2.jpg',0)
bus_LR3 = cv2.imread('buses/bus1_3.jpg',0)
bus_LR4 = cv2.imread('buses/bus1_4.jpg',0)
bus_LR5 = cv2.imread('buses/bus1_5.jpg',0)
bus_LR6 = cv2.imread('buses/bus1_6.jpg',0)
bus_LR7 = cv2.imread('buses/bus1_7.jpg',0)
bus_LR8 = cv2.imread('buses/bus1_8.jpg',0)
bus_LR9 = cv2.imread('buses/bus1_9.jpg',0)
bus_LR10 = cv2.imread('buses/bus1_10.jpg',0)
bus_LR11 = cv2.imread('buses/bus1_11.jpg',0)
bus_LR12 = cv2.imread('buses/bus1_12.jpg',0)
bus_LR13 = cv2.imread('buses/bus1_13.jpg',0)
bus_LR14 = cv2.imread('buses/bus1_14.jpg',0)
bus_LR15 = cv2.imread('buses/bus1_15.jpg',0)
bus_LR16 = cv2.imread('buses/bus1_16.jpg',0)
bus_LR17 = cv2.imread('buses/bus1_17.jpg',0)
bus_LR18 = cv2.imread('buses/bus1_18.jpg',0)
bus_LR19 = cv2.imread('buses/bus1_19.jpg',0)
bus_LR20 = cv2.imread('buses/bus1_20.jpg',0)
bus_LR22 = cv2.imread('buses/bus1_22.jpg',0)
bus_LR23 = cv2.imread('buses/bus1_23.jpg',0)
bus_LR24 = cv2.imread('buses/bus1_24.jpg',0)
bus_LR25 = cv2.imread('buses/bus1_25.jpg',0)

bus_RL1 = cv2.imread('buses/bus2_1.jpg',0)
bus_RL2 = cv2.imread('buses/bus2_2.jpg',0)
bus_RL3 = cv2.imread('buses/bus2_3.jpg',0)
bus_RL4 = cv2.imread('buses/bus2_4.jpg',0)
bus_RL5 = cv2.imread('buses/bus2_5.jpg',0)
bus_RL6 = cv2.imread('buses/bus2_6.jpg',0)
bus_RL7 = cv2.imread('buses/bus2_7.jpg',0)
bus_RL8 = cv2.imread('buses/bus2_8.jpg',0)
bus_RL9 = cv2.imread('buses/bus2_9.jpg',0)
bus_RL10 = cv2.imread('buses/bus2_10.jpg',0)
bus_RL11 = cv2.imread('buses/bus2_11.jpg',0)
bus_RL12 = cv2.imread('buses/bus2_12.jpg',0)

bus_LRNight1 = cv2.imread('buses/bus3_1.jpg',0)
bus_LRNight2 = cv2.imread('buses/bus3_2.jpg',0)
bus_LRNight3 = cv2.imread('buses/bus3_3.jpg',0)
bus_LRNight4 = cv2.imread('buses/bus3_4.jpg',0)
bus_LRNight5 = cv2.imread('buses/bus3_5.jpg',0)
bus_LRNight6 = cv2.imread('buses/bus3_6.jpg',0)
bus_LRNight7 = cv2.imread('buses/bus3_7.jpg',0)
bus_LRNight8 = cv2.imread('buses/bus3_8.jpg',0)
bus_LRNight9 = cv2.imread('buses/bus3_9.jpg',0)

bus_RLNight1 = cv2.imread('buses/bus4_1.jpg',0)
bus_RLNight2 = cv2.imread('buses/bus4_2.jpg',0)
bus_RLNight4 = cv2.imread('buses/bus4_4.jpg',0)
bus_RLNight5 = cv2.imread('buses/bus4_5.jpg',0)
bus_RLNight6 = cv2.imread('buses/bus4_6.jpg',0)
bus_RLNight7 = cv2.imread('buses/bus4_7.jpg',0)
bus_RLNight8 = cv2.imread('buses/bus4_8.jpg',0)
bus_RLNight9 = cv2.imread('buses/bus4_9.jpg',0)
bus_RLNight10 = cv2.imread('buses/bus4_10.jpg',0)
bus_RLNight11 = cv2.imread('buses/bus4_11.jpg',0)
bus_RLNight12 = cv2.imread('buses/bus4_12.jpg',0)
bus_RLNight13 = cv2.imread('buses/bus4_13.jpg',0)
bus_RLNight14 = cv2.imread('buses/bus4_14.jpg',0)
bus_RLNight15 = cv2.imread('buses/bus4_15.jpg',0)
bus_RLNight16 = cv2.imread('buses/bus4_16.jpg',0)
bus_RLNight17 = cv2.imread('buses/bus4_17.jpg',0)

templateBusesLR = [bus_LR1,
                   bus_LR2,
                   bus_LR3,
                   bus_LR4,
                   bus_LR5,
                   bus_LR6,
                   bus_LR7,
                   bus_LR8,
                   bus_LR9,
                   bus_LR10,
                   bus_LR11,
                   bus_LR12,
                   bus_LR13,
                   bus_LR14,
                   bus_LR15,
                   bus_LR16,
                   bus_LR17,
                   bus_LR18,
                   bus_LR19,
                   bus_LR20,
                   bus_LR22,
                   bus_LR23,
                   bus_LR24,
                   bus_LR25
                   ]

templateBusesRL = [bus_RL1,
                   bus_RL2,
                   bus_RL3,
                   bus_RL4,
                   bus_RL5,
                   bus_RL6,
                   bus_RL7,
                   bus_RL8,
                   bus_RL9,
                   bus_RL10,
                   bus_RL11,
                   bus_RL12
                   ]

templateBusesLRNight = [bus_LRNight1,
                        bus_LRNight2,
                        bus_LRNight3,
                        bus_LRNight4,
                        bus_LRNight5,
                        bus_LRNight6,
                        bus_LRNight7,
                        bus_LRNight8,
                        bus_LRNight9
                        ]

templateBusesRLNight = [bus_RLNight1,
                        bus_RLNight2,
                        bus_RLNight4,
                        bus_RLNight5,
                        bus_RLNight6,
                        bus_RLNight7,
                        bus_RLNight8,
                        bus_RLNight9,
                        bus_RLNight10,
                        bus_RLNight11,
                        bus_RLNight12,
                        bus_RLNight13,
                        bus_RLNight14,
                        bus_RLNight15,
                        bus_RLNight16,
                        bus_RLNight17
                        ]

def detectBus(grayFrame, template, threshold = 0.7):
    for temp in template:
        res = cv2.matchTemplate(grayFrame, temp, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        #print(maxVal)
        if maxVal > threshold:
            return True

