# OOP_Ex4
(Disclaimer: during this readme file i mention "we" quite a few times. That is purely for aesthetic and readability reasons, as this assignment was done by myself alone.)

This project is the fifth and final assignment in the course "Object Oriented Programming" in Ariel University, in which we use our implementation of a graph in the [previous project Ex3](https://github.com/danielzk107/OOP_Ex3) to write a program that plays a "Pokemon" game. The game itself is one where the player (in this case, our program) chases on-screen targets (pokemon) with a given value. The game itself is played on a directed-weighted graph (this is where the previous project is used), the targets stand on the edges, and the player moves from node to node. In this README file, we will learn how the project works, what libraries or algorithms it utilizes, and lastly, how to download and run it. If you are not intrested in how it works, you are welcome to skip straight and download it [here](https://www.youtube.com/watch?v=2ocykBzWDiM&t=0s).

## Implementation

### TBC

## GUI

### TBC

## Testing

The testing in this project uses the python library "unittest", and is rather elementary. There are two testing modules; one to test the graph (called GraphTests), and one to test the Algorithms (called AlgoTests). While the GraphTests module is identical to the one from the previous project (because it uses the same graph), the testing for the algorithms is unrelated to the one from Ex3, since the algorithms are different. The function which loads a graph from a json input works using a string in this project, and we get that string from the server, which can only accept one client at a time. As a result of that, in order to run the testing module for the algorithms, one first has to run the server with any scenario that uses the graph A3 (The tests were done using this specific graph). 

## Performance

### TBC

## How to run

### TBC
