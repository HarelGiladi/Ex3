import math


class GLocation:
    def __init__(self, pos:tuple=(0,0,0)):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

    def distance(self, other):
        tempx = math.pow((self.x - other.x), 2)
        tempy = math.pow((self.y - other.y), 2)
        tempz = math.pow((self.z - other.z), 2)
        return math.sqrt((tempx + tempy + tempz))

    def __str__(self):
        return "[" + self.x + ", " + self.y + ", " + self.z + "]"
