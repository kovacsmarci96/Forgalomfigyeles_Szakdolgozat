class Way:
    
    wayItems = 0

    def __init__(self,startP,length = 0,size=0,timer=0):
        self.Startp = startP
        self.endP = startP
        self.length = length
        self.size = size
        self.timer = timer
        Way.wayItems += 1

    def setEndP(self,point):
        self.endP = point


    def Timer(self):
        self.timer += 1

    def setLength(self,length):
        self.length = length

    def setSize(self,size):
        self.size = size
