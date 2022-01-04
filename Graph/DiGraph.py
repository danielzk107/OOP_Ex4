import Node
import Edge


class DiGraph:

    def __init__(self):
        self.nodelist = {}
        self.size = 0
        self.edgelist = {}
        self.modcount = 0

    def v_size(self) -> int:
        return self.size

    def e_size(self) -> int:
        return len(self.edgelist)

    def get_all_v(self) -> dict:
        return self.nodelist

    def all_in_edges_of_node(self, id1: int) -> dict:
        node = self.nodelist[id1]
        return node.inedgelistbyweight

    def all_out_edges_of_node(self, id1: int) -> dict:
        node = self.nodelist[id1]
        return node.outedgelistbyweight

    def get_mc(self) -> int:
        return self.modcount

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 not in self.nodelist or id2 not in self.nodelist:
            return False
        srcnode = self.nodelist[id1]
        destnode = self.nodelist[id2]
        if id2 in srcnode.outedgelist:
            return False
        edge = Edge.Edge(id1, id2, weight, len(self.edgelist))
        srcnode.AddEdge(id2, edge, 1)
        destnode.AddEdge(id1, edge, 0)
        self.edgelist[len(self.edgelist)] = edge
        self.modcount += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodelist:
            return False
        if pos is None:
            self.size += 1
            node = Node.Node(node_id, 0.0, 0.0, -1)
            self.nodelist[node_id] = node
            self.modcount += 1
            return True
        self.size += 1
        node = Node.Node(node_id, float(pos[0]), float(pos[1]), float(pos[2]))
        self.nodelist[node_id] = node
        self.modcount += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodelist:
            return False
        try:
            self.size -= 1
            node = self.nodelist[node_id]
            del self.nodelist[node_id]
            for x in node.inconnected:
                othernode = self.nodelist[x]
                edge = node.inedgelist[x]
                del self.edgelist[edge.idnum]
                othernode.RemoveEdge(node_id, 1)
            for x in node.outconnected:
                othernode = self.nodelist[x]
                edge = node.outedgelist[x]
                del self.edgelist[edge.idnum]
                othernode.RemoveEdge(node_id, 0)
        except IndexError:
            raise IndexError('One of the nodes/edges connected to node number ', node_id, ' is not in the graph')
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self.nodelist or node_id2 not in self.nodelist:
            return False
        node1 = self.nodelist[node_id1]
        node2 = self.nodelist[node_id2]
        if node_id2 not in node1.outedgelist:
            return False
        edge = node1.outedgelist[node_id2]
        del self.edgelist[edge.idnum]
        del node1.outedgelistbyweight[node_id2]
        del node1.outedgelist[node_id2]
        del node2.inedgelistbyweight[node_id1]
        del node2.inedgelist[node_id1]
        self.modcount += 1
        return True
