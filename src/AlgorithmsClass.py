import math
import json
import sys
from queue import PriorityQueue
from Graph import DiGraph
from Graph import Node


class Algorithms:

    def __init__(self, graph: DiGraph.DiGraph = None):
        if graph is None:
            self.graph = DiGraph.DiGraph()
        else:
            self.graph = graph
        self.modcount = self.graph.modcount
        self.ranSPD = False
        self.SPDlist = {}

    def find_edge(self, pokemon_pos: list, pokemon_type: int) -> int:  #  This function receives a position of a given "pokemon" and returns the id number of the edge it resides on.
        #  We check which edge is closest to the pokemon with a simple min function
        output = -1
        for edge in self.graph.edgelist:
            srcpoint = list()
            destpoint = list()
            srcpoint.append(self.graph.nodelist[self.graph.edgelist[edge].src].x)
            srcpoint.append(self.graph.nodelist[self.graph.edgelist[edge].src].y)
            destpoint.append(self.graph.nodelist[self.graph.edgelist[edge].dest].x)
            destpoint.append(self.graph.nodelist[self.graph.edgelist[edge].dest].y)
            if (self.distance(srcpoint, pokemon_pos) + self.distance(pokemon_pos, destpoint)) - self.distance(srcpoint, destpoint) < 0.0000001:
                if (pokemon_type == -1 and self.graph.edgelist[edge].src > self.graph.edgelist[edge].dest) or (pokemon_type == 1 and self.graph.edgelist[edge].src < self.graph.edgelist[edge].dest):
                    return edge
        return output

    def find_node(self, x: float, y: float) -> (int, Node):
        for nodeid in self.graph.nodelist:
            node = self.graph.nodelist[nodeid]
            if abs(node.x - x) <= 0.0000001 and abs(node.y - y) <= 0.0000001:
                return nodeid, node
        return -1, None

    def load_from_json(self, file_contents: str) -> bool:
        json_graph = json.loads(file_contents)
        for x in json_graph["Nodes"]:
            try:
                pos = str(x["pos"])
            except KeyError:
                pos = "0,0,-1"  # making z -1 to distinguish between position-less nodes and nodes with position (0,0)
            posarray = tuple(pos.split(","))
            self.graph.add_node(x["id"], posarray)
        for x in json_graph["Edges"]:
            id1 = int(str(x["src"]))
            id2 = int(str(x["dest"]))
            self.graph.add_edge(id1, id2, x["w"])
        return True

    def shortest_path_dist(self, src: int, dest: int) -> float:  #  The floyd-Warshal algorithm.
        if src == dest:
            return 0
        if self.ranSPD and self.modcount == self.graph.modcount:
            if self.SPDlist[src, dest] < 0 or self.SPDlist[src, dest] >= sys.float_info.max / 2:
                return float('inf')
            return self.SPDlist[src, dest]
        self.ranSPD = True
        self.modcount = self.graph.modcount
        # Setting all the values to the max num/to the weight of the edge:
        for x in self.graph.nodelist:
            xnode = self.graph.nodelist[x]
            for y in self.graph.nodelist:
                if y in xnode.outedgelist:
                    self.SPDlist[x, y] = xnode.outedgelist[y].weight
                else:
                    self.SPDlist[x, y] = sys.float_info.max / 2
        # Finding the best path for each two nodes:
        for x in self.graph.nodelist:
            for y in self.graph.nodelist:
                for z in self.graph.nodelist:
                    if self.SPDlist[y, z] > self.SPDlist[y, x] + self.SPDlist[x, z]:
                        self.SPDlist[y, z] = self.SPDlist[y, x] + self.SPDlist[x, z]
        return self.SPDlist[src, dest]

    def Dijkstra(self, id1: int, id2: int) -> (float, list):
        if id1 == id2:
            return 0, [0]
        # Simple Dijkstra's algorithm
        visited = list()
        parent = {}
        pq = PriorityQueue()
        dist = {x: float('inf') for x in self.graph.nodelist}
        dist[id1] = 0
        pq.put((0, id1))
        parent[id1] = -1
        while not pq.empty():
            (x, curr) = pq.get()
            visited.append(curr)
            for neighbor in self.graph.nodelist:
                node = self.graph.nodelist[neighbor]
                if curr in node.inedgelistbyweight:
                    distance = node.inedgelistbyweight[curr]
                    if node.idnum not in visited:
                        if dist[curr] + distance < dist[node.idnum]:
                            dist[node.idnum] = dist[curr] + distance
                            pq.put((dist[curr] + distance, node.idnum))
                            parent[neighbor] = curr
        if id2 not in parent:
            return float('inf'), None
        output = self.getlistofparent(id2, parent, list())
        output.reverse()
        return dist[id2], output

    def getlistofparent(self, idnum: int, parent: dict, l: list) -> list:
        node = self.graph.nodelist[idnum]
        node.tag = 1
        l.append(idnum)
        if parent[idnum] == -1:
            return l
        return self.getlistofparent(parent[idnum], parent, l)

    def distance(self, point_a: list, point_b: list):
        return math.sqrt(math.pow((point_a[0]-point_b[0]), 2) + math.pow((point_a[1]-point_b[1]), 2))

