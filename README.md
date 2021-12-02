# euler-circuit
This project is a backtracking algorithm to find an Euler circuit in a graph if one exists or to identify when there isn't one. 

## Description
There are simple ways of determining whether a given graph has an Euler circuit, and this should be checked before starting to find an actual Euler circuit.

A backtracking algorithm to build an Euler circuit is a recursive algorithm which tries in a systematic way all the possible ways of building a circuit and stops when it manages to build one. More precisely, it can be described as a recursive function which tries to visit the "next" available vertex (i.e. one which is joined to the current vertex by an unvisited edge) until an Euler circuit is found. Visiting the next vertex consists of:

1) Adding the vertex to the circuit
2) Trying to visit each of its available adjacent vertices one by one, each time trying to complete a Euler circuit, until you find one that works, in which case the circuit has been built. An "available adjacent vertex" is one which shares a still unvisited adjacent edge with the vertex being visited.
3) If it was not possible to visit an available adjacent vertex, then the visit of the original vertex failed, and it should be removed from the circuit.

## Execution
When executing, make sure you run the "Test.py" file. The file, "Test.py" redirects the path toward the directory "/tests". Inside "/tests", there are multiple test cases that my program handles. We can also define our own test cases and try running them. 


## Author
Hadi Awan
