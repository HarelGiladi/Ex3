class Edge:

    def __init__(self, src: int, dst: int, weight: float):
        self.src = src
        self.dst = dst
        self.weight = weight
        self.info = "White"
        self.tag = -1

    def __str__(self):
        return "Edge{src= "+self.src+", dest= "+self.dst+", weight= "+self.weight+"}"
    