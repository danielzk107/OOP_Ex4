import unittest
import DiGraph


class GraphTests(unittest.TestCase):

    def test_addnode(self):
        graph = DiGraph.DiGraph()
        self.assertTrue(graph.add_node(0))
        self.assertTrue(graph.add_node(1))
        self.assertTrue(graph.add_node(2))
        self.assertTrue(graph.add_node(3))
        self.assertTrue(graph.add_node(4), (1, 3, 5))
        self.assertTrue(graph.add_node(5), (0, 90, 24))

    def test_addedge(self):
        graph = DiGraph.DiGraph()
        self.assertFalse(graph.add_edge(0, 2, 4))
        self.assertFalse(graph.add_edge(0, 5, 8))
        self.assertFalse(graph.add_edge(3, 2, 9.4))
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        self.assertTrue(graph.add_edge(0, 3, 0.42))
        self.assertTrue(graph.add_edge(0, 1, 3.52))
        self.assertTrue(graph.add_edge(0, 2, 6.45))
        self.assertTrue(graph.add_edge(3, 2, 1.345))

    def test_removenode(self):
        graph = DiGraph.DiGraph()
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4, (1, 3, 5))
        graph.add_node(5, (0, 90, 24))
        graph.add_edge(0, 3, 0.42)
        graph.add_edge(0, 1, 3.52)
        self.assertTrue(graph.remove_node(0))
        self.assertFalse(0 in graph.nodelist)
        self.assertFalse(0 in graph.nodelist[3].inedgelist)

    def test_removeedge(self):
        graph = DiGraph.DiGraph()
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)
        graph.add_node(4, (1, 3, 5))
        graph.add_node(5, (0, 90, 24))
        graph.add_edge(0, 3, 0.42)
        graph.add_edge(0, 1, 3.52)
        self.assertTrue(graph.remove_edge(0, 3))
        self.assertTrue(graph.remove_edge(0, 1))
        self.assertFalse(0 in graph.nodelist[3].inedgelist)
        self.assertFalse(0 in graph.nodelist[1].inedgelist)


if __name__ == '__main__':
    unittest.main()