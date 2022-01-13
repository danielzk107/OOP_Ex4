# OOP_Ex4
(Disclaimer: during this readme file i mention "we" quite a few times. That is purely for aesthetic and readability reasons, as this assignment was done by myself alone.)

This project is the fifth and final assignment in the course "Object Oriented Programming" in Ariel University, in which we use our implementation of a graph in the [previous project Ex3](https://github.com/danielzk107/OOP_Ex3) to write a program that plays a "Pokemon" game. The game itself is one where the player (in this case, our program) chases on-screen targets (pokemon) with a given value. The game is played on a directed-weighted graph (this is where the previous project is used), the targets stand on the edges, and the player moves from node to node. In this README file, we will learn how the project works, what libraries or algorithms it utilizes, and lastly, how to download and run it. If you are not intrested in how it works, you are welcome to skip straight and download it [here](https://www.youtube.com/watch?v=2ocykBzWDiM&t=0s).

## Implementation

Like mentioned previously, this projects uses the graph implementation of the previous project, Ex3. Therefore, in this chapter we will only discuss the module where this project differs from the last one: the Algorithms class. To read the full explanation of the graph implementation, click [here](https://github.com/danielzk107/OOP_Ex3#implementation). 

### AlgorithmsClass

The Algorithms Class is the class that both loads the graph from a Json string, and helps the main movement algorithm (inside the GUI classs) by calculating the distances and most efficient paths between nodes. This class contains less functions and algorithms than its previous rendition in Ex3, but is still very similar. It has five functions; find_edge, find_node, load_from_json, shortest_path_dist, and Dijkstra.

#### find_edge

This function receives a set of coordinates (of a pokemon) and returns the id number of the edge it is closest to (or -1 if it is not significantly close to any edge). 
It does so by looping through all the edges in the graph and checking whether the distance between the coordinates and the source and destination of the edge (put together) is (roughly) equal to the length of that edge. If so, it returns the id number of the edge.

#### find_node

This function receives a set of coordinates and returns the id number of the node it is closest to (of -1 if it is not significantly close to any node).
It does so by looping through all the nodes in the graph and checking whether the position of the current node is roughly equal to the given coordinates. If so, it returns the id number of the node.

#### load_from_json

This function receives a string that is formatted in in a json format (if not the function will raise an exception) and creates a graph according to the instructions written inside it.

#### shortest_path_dist

This function receives two integers, which represent two node id numbers, and outputs the shortest distance between them. The function is a python implementation of the [Floyd-Warshall algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm) using dynamic programming. During its first run, the function calculates all the shortest distances between every two nodes and puts them in a dictionary. when it is finished it returns the requested answer, and the next time it will be called - instead of calculating, the answer will be immediately returned from the dictionary where it was stored, with O(1) actions.

#### Dijkstra

This function receives two integers, which represent two node id numbers, and outputs the shortest distance and shortest path between them. That is, it returns the distance as a number, and also returns the path as an ordered list. The function is a python implementation of [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm).


## GUI

This project uses Pygame, which is an open-source GUI for python, used mostly for casual game development (not serious gaming, as python is too slow). In the GUI the nodes are represented by a picture of a pokemon center, the player by a picture of Ash Ketchum, the downwards pokemon by a picture of bulbasaur, and the upwards pokemon by a picture of charizard. Here is a short gif of the GUI when running scenario number 13 (sped up x1.5):

![Pokémon_Game_vid_Trim](https://user-images.githubusercontent.com/92798950/149381130-8f55cc59-bd90-45c8-b1b9-ac52f08ab87c.gif)


## Testing

The testing in this project uses the python library "unittest", and is rather elementary. There are two testing modules; one to test the graph (called GraphTests), and one to test the Algorithms (called AlgoTests). While the GraphTests module is identical to the one from the previous project (because it uses the same graph), the testing for the algorithms is unrelated to the one from Ex3, since the algorithms are different. The function which loads a graph from a json input works using a string in this project, and we get that string from the server, which can only accept one client at a time. As a result of that, in order to run the testing module for the algorithms, one first has to run the server with any scenario that uses the graph A3 (The tests were done using this specific graph). 

## Performance

The performance of this program is measured directly by the server that runs it. Here is a table with all the scenarios and their respective grades:

| Scenario | Grade |
| --- | --- |
| 0 | 85 |
| 1 | 526 |
| 2 | 249 |
| 3 | 853 |
| 4 | 171 |
| 5 | 474 | 
| 6 | 79 |
| 7 | 279 |
| 8 | 52 |
| 9 | 331 |
| 10 | 88 |
| 11 | 419 |
| 12 | 31 |
| 13 | 147 |
| 14 | 67 |
| 15 | 229 |

## How to run
In order to run this project, one has to download both the client code (the code shared here) and the server side (the jar file in the main branch). Once downloaded, open the command line/terminal and go to the file path of the jar file you have downloaded, then type in 'java -jar Ex4_Server_v0.0.jar #' and replace the # with any number you would like between 0 and 15. The server should respond with the message 'init Ex4 server with case: #'. After you have run the server, open this project in an IDE of your choice and run the file 'main.py'. After that, you should see the game window po up and the game would start playing.
If you are experiencing any difficulties in any of these steps, you are welcome to ask for technical support from danielzk107@gmail.com
