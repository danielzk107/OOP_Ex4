import json
from time import sleep
from types import SimpleNamespace
import random
import pygame
from pygame import *
from pygame import gfxdraw
from Graph import Node
from Graph import Edge
from client import Client
from src.AlgorithmsClass import Algorithms


class GUI:

    def __init__(self, g_algo: Algorithms, client: Client):
        self.g_algo = g_algo
        self.client = client
        pygame.init()
        self.screen = display.set_mode((800, 600), depth=32, flags=RESIZABLE)

    def scale(self, x: float, y: float) -> (float, float):
        output_x = ((x - self.g_algo.graph.min_x)/(self.g_algo.graph.max_x - self.g_algo.graph.min_x)) * (self.screen.get_width() - 100) + 50  #Using the same scaling formula as the example
        output_y = ((y - self.g_algo.graph.min_y)/(self.g_algo.graph.max_y - self.g_algo.graph.min_y)) * (self.screen.get_height() - 100) + 50  #Using the same scaling formula as the example
        return output_x, output_y

    def play(self):
        clock = pygame.time.Clock()
        self.client.add_agent("{\"id\":0}")
        self.client.start()
        running = self.client.is_running() == 'true'
        count = 0
        bglist = list()
        bglist.append((99, 108, 121))
        bglist.append((113, 125, 144))
        bglist.append((113, 144, 139))
        while running:
            self.screen.fill((99, 108, 121))
            running = self.client.is_running() == 'true'
            pokemons = json.loads(self.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for p in pokemons:
                print(p)
            for edge in self.g_algo.graph.edgelist:
                self.print_edge(self.g_algo.graph.edgelist[edge])
            for node in self.g_algo.graph.nodelist:
                self.print_node(self.g_algo.graph.nodelist[node])
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    print(mouse)
            clock.tick(60)
            count += 1

    def print_node(self, node: Node.Node):
        FONT = pygame.font.SysFont('Arial', 20, bold=True)
        x, y = self.scale(node.x, node.y)
        pygame.draw.circle(self.screen, pygame.color.Color((228, 164, 68)), (x, y), 10)
        id_srf = FONT.render(str(node.idnum), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        self.screen.blit(id_srf, rect)
        gfxdraw.aacircle(self.screen, int(x), int(y), 10, pygame.color.Color((228, 164, 68)))

    def print_edge(self, edge: Edge.Edge):
        srcnode = self.g_algo.graph.nodelist[edge.src]
        destnode = self.g_algo.graph.nodelist[edge.dest]
        pygame.draw.line(self.screen, pygame.color.Color((228, 164, 203)), self.scale(srcnode.x, srcnode.y), self.scale(destnode.x, destnode.y), 2)

