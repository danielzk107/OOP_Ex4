from Graph import Edge


class Node:
    def __init__(self, idnum: int, x: float, y: float, z: float):
        self.idnum = idnum
        self.x = x
        self.y = y
        self.z = z
        self.tag = 0
        self.inconnected = list()
        self.outconnected = list()
        self.inedgelist = {}
        self.inedgelistbyweight = {}
        self.outedgelist = {}
        self.outedgelistbyweight = {}

    def AddEdge(self, otherid: int, edge: Edge.Edge, direction: int):  #if direction is 1, the edge goes out, if it is 0, then the edge goes in.
        if direction == 1:
            if otherid not in self.outedgelist:
                self.outedgelist[otherid] = edge
                self.outedgelistbyweight[otherid] = edge.weight
                self.outconnected.append(otherid)
        else:
            if otherid not in self.inedgelist:
                self.inedgelist[otherid] = edge
                self.inedgelistbyweight[otherid] = edge.weight
                self.inconnected.append(otherid)

    def RemoveEdge(self, otherid: int, direction: int) -> Edge:
        output = None
        if direction == 1:
            if otherid in self.outedgelist:
                output = self.outedgelist[otherid]
                del self.outedgelist[otherid]
                del self.outedgelistbyweight[otherid]
                self.outconnected.remove(otherid)
        else:
            if otherid in self.inedgelist:
                output = self.inedgelist[otherid]
                del self.inedgelist[otherid]
                del self.inedgelistbyweight[otherid]
                self.inconnected.remove(otherid)
        return output
