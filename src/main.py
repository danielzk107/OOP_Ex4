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

HOST = "127.0.0.1"
PORT = 6666
# Create a connection:
client = Client()
client.start_connection(HOST, PORT)
pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
print(pokemons)
# Create an algorithms object and get a graph:
g_algo = Algorithms()
g_algo.load_from_json(client.get_graph())


