import math
import json
import sys

from Graph import DiGraph
from Graph import Node
from Graph import Edge


class Algorithms:

    def __init__(self, graph: DiGraph.DiGraph = None):
        if graph is None:
            self.graph = DiGraph.DiGraph()
        else:
            self.graph = graph
        self.modcount = self.graph.modcount
        self.ranSPD = False
        self.SPDlist = {}

    def find_edge(self, pokemon_pos: list) -> int:  #This function receives a position of a given "pokemon" and returns the id number of the edge it resides on.
        for edge in self.graph.edgelist:
            srcpoint = list()
            destpoint = list()
            srcpoint.append(edge.src.x)
            srcpoint.append(edge.src.y)
            destpoint.append(edge.dest.x)
            destpoint.append(edge.dest.y)
            if (self.distance(srcpoint, pokemon_pos) + self.distance(pokemon_pos, srcpoint)) == self.distance(srcpoint, destpoint):
                return edge.idnum
        return -1

    def load_from_json(self, file_name: str) -> bool:
        try:
            temp = open(file_name, 'r')
            jsonfile = json.load(temp)
            for x in jsonfile["Nodes"]:
                try:
                    pos = str(x["pos"])
                except KeyError:
                    pos = "0,0,-1"  # making z -1 to distinguish between position-less nodes and nodes with position (0,0)
                posarray = tuple(pos.split(","))
                self.graph.add_node(x["id"], posarray)
            for x in jsonfile["Edges"]:
                id1 = int(str(x["src"]))
                id2 = int(str(x["dest"]))
                self.graph.add_edge(id1, id2, x["w"])
        except FileNotFoundError:
            temp.close()
            raise Exception("File not found")
        except TypeError:
            temp.close()
            raise Exception("The given file is not formatted correctly")
        except Exception:
            temp.close()
            raise Exception("Unknown problem arose")
        temp.close()
        return True

    def save_to_json(self, file_name: str) -> bool:
        try:
            temp = open(file_name, 'r')
            print("File already exists")
            temp.close()
            return False
        except FileNotFoundError:
            try:
                with open(file_name, 'w', newline="") as newfile:
                    nodeslist = list()
                    for x in self.graph.nodelist:
                        pos = (self.graph.nodelist[x].x, self.graph.nodelist[x].y, self.graph.nodelist[x].z).__str__()
                        temp = pos.replace("(", "")
                        newpos = temp.replace(")", "")
                        nodeslist.append({"id": self.graph.nodelist[x].idnum, "pos": newpos})
                    edgeslist = list()
                    for x in self.graph.edgelist:
                        edgeslist.append({"src": self.graph.edgelist[x].src, "dest": self.graph.edgelist[x].dest,
                                          "w": self.graph.edgelist[x].weight})
                    json.dump({"Nodes": nodeslist, "Edges": edgeslist}, newfile, indent=4)
            except FileExistsError:
                raise Exception("File already exists")
            except Exception:
                newfile.close()
                raise Exception("Unknown problem arose")
            newfile.close()
            return True

    def shortest_path_dist(self, src: int, dest: int) -> float:  #The floyd-Warshal algorithm.
        if src == dest:
            return float('inf')
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

    def distance(self, point_a: list, point_b: list):
        return math.sqrt(math.pow((point_a[0]-point_b[0]), 2) + math.pow((point_a[1]-point_b[1]), 2))

