class Way:
    
    wayItems = 0

    def __init__(self,startP,timer=0):
        self.Startp = startP
        self.endP = startP
        self.timer = timer
        Way.wayItems += 1

    def setEndP(self,point):
        self.endP = point

    def Timer(self):
        self.timer += 1
