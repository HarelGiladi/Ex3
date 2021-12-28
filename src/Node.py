import sys

import GLocation


class Node:
    # can make problams maybe we should do without startkeys
    startKeys = 0

    def __init__(self, key: int, location: GLocation):
        if key == None:
            self.key = Node.startKeys
            Node.startKeys += 1
        else:
            self.key = key
            Node.startKeys += 1
        self.location = location
        self.weight = sys.float_info.max
        self.info = "white"
        self.tag = -1

    def __str__(self):
        # return "Node{key= "+self.key+ ", weight= "+self.weight +", info= "+self.info+", tag= "+self.tag+"}"
        return "Node{key= " + self.key + "}"
