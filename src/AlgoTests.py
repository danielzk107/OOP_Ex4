import json
import unittest

import self as self

import AlgorithmsClass
from src.client import Client

#  Run on scenarios 12 - 15 (All the tests work on the graph A3)


class TestGraphAlgo(unittest.TestCase):

    def test_allfunctions(self):  # Because we need to connect to the server, and can only do it once, the testing will be done in one function
        HOST = "127.0.0.1"
        PORT = 6666
        client = Client()
        client.start_connection(HOST, PORT)
        algo = AlgorithmsClass.Algorithms()
        algo.load_from_json(client.get_graph())
        #  Test Dijkstra's algorithm:
        self.assertEqual(algo.Dijkstra(1, 25), (6.564794450458431, [1, 0, 22, 23, 24, 25]))
        self.assertEqual(algo.Dijkstra(4, 37), (10.536959491272517, [4, 5, 6, 7, 8, 35, 36, 37]))
        self.assertEqual(algo.Dijkstra(0, 0), (0, [0]))
        self.assertEqual(algo.Dijkstra(2, 66), (float('inf'), None))
        self.assertEqual(algo.Dijkstra(42, 12), (float('inf'), None))
        self.assertEqual(algo.Dijkstra(2, 66), (float('inf'), None))
        #  Test Find_edge:
        self.assertEqual(algo.find_edge([35.20392770907119, 32.10833067124629], 1), 80)
        self.assertEqual(algo.find_edge([35.20622459040522, 32.101281022067994], 1), 40)
        self.assertEqual(algo.find_edge([35.21233170626735, 32.10466952803471], 1), 29)
        self.assertEqual(algo.find_edge([35.21200574506042, 32.105721621191464], 1), 27)
        self.assertEqual(algo.find_edge([35.21200574674589, 32.105236534156361], 1), -1)
        self.assertEqual(algo.find_edge([35.23465498702213, 32.654032069873680], 1), -1)
        #  Test Find_Node:
        idnum, _ = algo.find_node(35.19742222276029, 32.1051815882353)
        self.assertEqual(idnum, 3)
        idnum, _ = algo.find_node(35.1988444180791, 32.103727739495795)
        self.assertEqual(idnum, 4)
        idnum, _ = algo.find_node(35.195575491525425, 32.10349148907563)
        self.assertEqual(idnum, 25)
        idnum, _ = algo.find_node(35.21315127845036, 32.10427293277311)
        self.assertEqual(idnum, 12)
        idnum, _ = algo.find_node(35.21315127845036, 32.06510323546695)
        self.assertEqual(idnum, -1)
        idnum, _ = algo.find_node(35.98765406506353, 32.10427293277311)
        self.assertEqual(idnum, -1)
        #  Test shortest_path_dist:
        self.assertEqual(algo.shortest_path_dist(1, 23), 2.699458615873293)
        self.assertEqual(algo.shortest_path_dist(4, 19), 7.684693820505638)
        self.assertEqual(algo.shortest_path_dist(25, 7), 5.021389181767592)
        self.assertEqual(algo.shortest_path_dist(6, 6), 0)
        self.assertEqual(algo.shortest_path_dist(29, 7), 5.371692964385201)
        self.assertEqual(algo.shortest_path_dist(0, 26), 7.191081596128457)
        self.assertEqual(algo.shortest_path_dist(1, 28), 3.3337461139018814)
        self.assertEqual(algo.shortest_path_dist(18, 26), 9.991798776722392)
        client.stop_connection()


if __name__ == '__main__':
    unittest.main()