import json
import sys
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
        caught_current_pokemon = True
        up_image = pygame.image.load("../data/charizard.png")
        down_image = pygame.image.load("../data/bulbasaur.png")
        agent_image = pygame.image.load("../data/ash.png")
        next_target_by_agent = {}  #  A dictionary which keeps the next target for every agent
        pokemonlist_by_edge = {}  #  keeps each pokemon by the edge it is on
        caught_pokemon_for_each_agent = {}  #  A dictionary of lists which keeps the pokemon each agent caught
        agents = json.loads(self.client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents = [agent.Agent for agent in agents]
        for agent in agents:
            caught_pokemon_for_each_agent[agent.id] = list()
        while self.client.is_running() == 'true' and running:
            self.screen.fill((99, 108, 121))
            running = self.client.is_running() == 'true'
            pokemons = json.loads(self.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for p in pokemons:
                pokemon_type = int(p.type)
                x, y, _ = p.pos.split(',')
                pos_list = list()
                pos_list.append(float(x))
                pos_list.append(float(y))
                x, y = self.scale(float(x), float(y))
                #  Find which edge the pokemon is on
                pokemonlist_by_edge[self.g_algo.find_edge(pos_list, pokemon_type)] = p
                if pokemon_type == 1:
                    self.screen.blit(pygame.transform.scale(up_image, (45, 30)), (x, y))
                else:
                    self.screen.blit(pygame.transform.scale(down_image, (45, 30)), (x, y))
                # pygame.draw.circle(self.screen, pygame.color.Color((67, 194, 168)), (x, y), 12.5)
            for edge in self.g_algo.graph.edgelist:
                self.print_edge(self.g_algo.graph.edgelist[edge])
            for node in self.g_algo.graph.nodelist:
                self.print_node(self.g_algo.graph.nodelist[node])
            for a in agents:
                x, y, _ = a.pos.split(',')
                x, y = self.scale(float(x), float(y))
                self.screen.blit(pygame.transform.scale(agent_image, (45, 30)), (x, y))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    print(mouse)
            #  Temporary function to move the agent
            agents = json.loads(self.client.get_agents(), object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for agent in agents:
                #  We calculate the potential gain of each pokemon (we then take the one where (distance_from_agent - value) is the smallest)
                x, y, _ = agent.pos.split(',')
                nodeid, node = self.g_algo.find_node(float(x), float(y))
                if agent.dest == -1:
                    if agent.id not in next_target_by_agent:
                        next_target_by_agent[agent.id] = None
                    pos_by_value_and_dist = {}  #  Keeps the edge of each pokemon with the distance and value as a key
                    # print(pokemonlist_by_edge)
                    for p in pokemonlist_by_edge:
                        edge = self.g_algo.graph.edgelist[p]
                        if pokemonlist_by_edge[p] not in caught_pokemon_for_each_agent[agent.id]:
                            pos_by_value_and_dist[self.g_algo.shortest_path_dist(nodeid, edge.src) + self.g_algo.shortest_path_dist(edge.src, edge.dest), pokemonlist_by_edge[p].value] = edge
                    selected_pokemon_pos = None
                    best_potential_gain = sys.float_info.max
                    if caught_current_pokemon or next_target_by_agent[agent.id] is None or pokemonlist_by_edge[next_target_by_agent[agent.id].idnum] in caught_pokemon_for_each_agent[agent.id]:
                        print(pos_by_value_and_dist)
                        for key in pos_by_value_and_dist:
                            dist, value = key
                            if dist - value < best_potential_gain:
                                best_potential_gain = dist - value
                                selected_pokemon_pos = pos_by_value_and_dist[key]
                        caught_current_pokemon = False
                        next_target_by_agent[agent.id] = selected_pokemon_pos
                        print("new target: from " + str(self.g_algo.graph.edgelist[next_target_by_agent[agent.id].idnum].src) + " to " + str(str(self.g_algo.graph.edgelist[next_target_by_agent[agent.id].idnum].dest)) + " with value of " + str(pokemonlist_by_edge[next_target_by_agent[agent.id].idnum].value))
                    if next_target_by_agent[agent.id] is not None and agent.src != next_target_by_agent[agent.id].src:
                        dist, path = self.g_algo.Dijkstra(nodeid, next_target_by_agent[agent.id].src)
                        print(path[1])
                        self.client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(path[1]) + '}')
                    else:
                        if next_target_by_agent[agent.id] is not None:
                            self.client.choose_next_edge(
                                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_target_by_agent[agent.id].dest) + '}')
                            caught_current_pokemon = True
                            caught_pokemon_for_each_agent[agent.id].append(pokemonlist_by_edge[next_target_by_agent[agent.id].idnum])
                            print("Caught pokemon")
                            print(caught_pokemon_for_each_agent[agent.id])
                self.client.move()
            pygame.display.update()
            # sleep(0.2)
            clock.tick(60)

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


