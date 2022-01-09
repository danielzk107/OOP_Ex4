"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
import Graph
from AlgorithmsClass import Algorithms
from pygame import gfxdraw
import pygame
from pygame import *
from src import GUI

HOST = "127.0.0.1"
PORT = 6666
# Create a connection:
client = Client()
client.start_connection(HOST, PORT)
pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
# Create an algorithms object and get a graph:
g_algo = Algorithms()
g_algo.load_from_json(client.get_graph())

#  Using the given method for obtaining the minimum and maximum values of x and y in the graph:
graph = json.loads(client.get_graph(), object_hook=lambda json_dict: SimpleNamespace(**json_dict))
for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

g_algo.graph.min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
g_algo.graph.min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
g_algo.graph.max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
g_algo.graph.max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y

gui = GUI.GUI(g_algo, client)
print("Calling the run function")
gui.play()




