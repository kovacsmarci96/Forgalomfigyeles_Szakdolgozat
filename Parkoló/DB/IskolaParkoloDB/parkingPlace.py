class parkingPlace:

    def __init__(self,rect):
        self.corner1 = rect[0]
        self.corner2 = rect[1]
        self.corner3 = rect[2]
        self.corner4 = rect[3]

        self.minx = self.corner1[0]
        if self.corner2[0] < self.minx:
            self.minx = self.corner2[0]

        self.miny = self.corner1[1]
        if self.corner4[1] < self.miny:
            self.miny = self.corner4[1]

        self.maxx = self.corner3[0]
        if self.corner4[0] > self.maxx:
            self.maxx = self.corner4[0]

        self.maxy = self.corner2[1]
        if self.corner3[1] > self.maxy:
            self.maxy = self.corner3[1]
