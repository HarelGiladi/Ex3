import math


class GLocation:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        tempx = math.pow((self.x - other.x), 2)
        tempy = math.pow((self.y - other.y), 2)
        tempz = math.pow((self.z - other.z), 2)
        return math.sqrt((tempx + tempy + tempz))

    def __str__(self):
        return "[" + self.x + ", " + self.y + ", " + self.z + "]"
