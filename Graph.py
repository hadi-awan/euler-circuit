from Walk import Walk
import sys
import random
import copy

sys.setrecursionlimit(100000)

class Graph:
    """
    Graph objects can be used to work with undirected graphs.
    They are internally represented using adjacency matrices.
    """
    DIRECTED = True
    UNDIRECTED = False
    seeded = False
	  
    @classmethod
    def fromFile(cls, filename):
        """
	Instantiates list of Graphs read from a file.  The file has the following format:
            Each graph starts on a new line which contains two elements: 
                - "D" or "U" to specify whether the graph is directed or undirected
                - The number of vertices in that graph
            Followed by one line for each row of the adjacency matrix of the graph: 
                in each row the elements are separated by blanks.
	
	Note: When it encounters problems with the data, fromFile stops reading the file and
	returns the correct information read up to that point.
	 
	Parameters:
            str filename: name of file containing graphs
	
	Returns a list of Graphs described in the file. 
	"""
        f = open(filename, "r")
        graphList = []
        with f as lines:
            row = 0
            for line in lines:
                if row == 0:
                    entries = line.split()
                    if len(entries) != 2:
                        print("Error: First line of graph must have format 'D'|'U' ertices")
                        break
                    if entries[0]=='U':
                        directed = Graph.UNDIRECTED
                    else:
                        directed = Graph.DIRECTED
                    vertices = int(entries[1])
                    edges = []
                    row += 1
                elif row <= vertices:
                    newrow = [int(i) for i in line.split()]
                    if len(newrow) != vertices:
                        print("Error: invalid number of entries in row ", row)
                        break
                    edges.append(newrow)
                    row += 1
                elif row > vertices:
                    graphList.append(Graph(directed, vertices, edges))
                    row = 0
        f.close()
        return graphList
    
    @classmethod
    def newRandomSimple(cls, seed, vertices, density):
        """
	Instantiates new simple Graph randomly as specified by parameters.
	The graph is undirected without loops or parallel edges.
	 
	Parameters:
            int seed: seed for random number generator
            int vertices: number of vertices in the Graph
            int density: the odds that there will be an edge between any two distinct vertices are 1/density

	Returns a new graph to specifications or None if they can't be met.
	"""

        if vertices <= 0:
            print("Error: Number of vertices must be positive")
            return None
        if density <= 1:
            print("Error: density must be greater than 1")
            return None
        # Seed the random number generator once
        if not Graph.seeded:
            random.seed(a=seed)
            Graph.seeded = True

        # Create array of 0 edges
        edges = []
        for i in range(vertices):
            edges.append(list([0]*vertices))

        # Populate non-diagonal cells of matrix
        for i in range(vertices):
            for j in range(i+1,vertices):
                if random.randint(0, density-1) == density-1:                
                    edges[i][j] = 1
                edges[j][i] = edges[i][j]
        return Graph(Graph.UNDIRECTED, vertices, edges)

    def __init__(self, directed, vertices, edges):
        """Creates a new Graph from an adjacency matrix
	
	Parameters:
            Boolean directed: Graph.DIRECTED or Graph.UNDIRECTED
            int vertices: number of vertices in the Graph
            List edges: adjacency matrix of the edges
	
	Notes:
	- This constructor is not intended to be used directly.
	  The two class methods fromFile and newRandomSimple should be used instead.
	- Nevertheless, if incorrect data is received, the graph information will be rejected
          and an empty graph will be returned.
	"""
        self.inputMistakes = False
        self.directed = directed
        if vertices <= 0:
            print("Error: Number of vertices must be positive")
            return
        
        # Total number of vertices and edges.
        self.totalV = vertices
        self.totalE = 0
        
        # Adjacency matrix of graph.
        # edges[x][y] is the number of edges from vertex x to vertex y.
        self.edges = edges
        
        # Used by graph visitors to keep track of visited vertices.
        self.visitedV = [None]*vertices
        
        # Used by graph visitors to keep track of visited edges.
        self.visitedE = []
        
        # Used by graph visitors to keep track of unvisited edges
        # as an alternative to using visitedE.
        self.unvisitedE = []
        
        for i in range(vertices):
            self.visitedE.append(list([None]*vertices))
            self.unvisitedE.append(list([None]*vertices))
        self.clearVisited()
        
        # Read adjacency matrix
        for i in range(vertices):
            for j in range(vertices):
                if edges[i][j] < 0:
                    print("Error: Number of edges cannot be negative")
                    self.inputMistakes = True
                elif directed or j >= i:
                    self.totalE += edges[i][j]
        
        # Verify that adjacency matrix is symmetric when graph is undirected
        if not directed:
            for i in range(vertices):
                for j in range(i+1, vertices):
                    if edges[i][j] != edges[j][i]:
                        print("Error: adjacency matrix is not symmetric")
                        self.inputMistakes = True
        if self.inputMistakes:
            self.totalV = 0

    def clearVisited(self):
        """Resets visitedV, visitedE, and unvisitedE matrices for a new visitation."""
        for i in range(self.totalV):
            self.visitedV[i] = False
            for j in range(self.totalV):
                self.visitedE[i][j] = 0
                self.unvisitedE[i][j] = self.edges[i][j]

    def __str__(self):
        """Returns a String representation of the graph
        which is a 2-D representation of the adjacency matrix of that graph."""
        res = ""
        for i in range(self.totalV):
            for j in range(self.totalV-1):
                res += str(self.edges[i][j])
                res += " "
            res += str(self.edges[i][self.totalV-1])
            res += "\n"
        return res

    def totalVertices(self):
        """Returns the number of vertices in the graph."""
        return self.totalV

    def totalEdges(self):
        """Returns the number of edges in the graph."""
        return self.totalE

    def getEdges(self):
        """Returns a deep copy of the adjacency matrix of the graph."""
        return copy.deepcopy(self.edges)

    def getEdgeCount(self, sourceV, destV):
        """
        Counts number of edges between two vertices

        Parameters:
            int sourceV: sourve vertex
            int destV: destination vertex

        Returns the number of edges from sourceV to destV
        """
        if sourceV >= 0 and sourceV < self.totalV and destV >= 0 and destV < self.totalV:
            return self.edges[sourceV][destV]
        else:
            return 0

    def isConnected(self):
        """Returns True iff graph is connected."""
        self.clearVisited()
        self.DFSvisit(0)
        for i in range(self.totalV):
            if not self.visitedV[i]:
                return False
        return True

    def DFSvisit(self, vertex):
        """
        Conducts a Depth First Search visit of the unvisited vertices.
        Ties between vertices are broken in numeric order.

        Parameters:
            int vertex: starting vertex for the DFS visit

        Side Effect:
            visitedV is updated to reflect which vertices are visited.
        """
        self.visitedV[vertex] = True
        for i in range(self.totalV):
            if self.edges[vertex][i] != 0 and not self.visitedV[i]:
                self.DFSvisit(i)

    def findEuler(self):
        """
        Returns: an Euler circuit for the graph if one exists,
        or None if none exists.
        """
        # TODO: 
        """
        - check that it's connected
        """
        startingVertex = 0
        self.clearVisited()
        walk = Walk(self.totalEdges()+ 1)
        
        if self.tryVisiting(startingVertex, self.totalEdges(), walk):
            
            return walk
        else:
            return None
        


    def tryVisiting(self, vertex, unvisitedEs, walk):
        """
        Recursive backtracking algorithm tries visiting adjacent unvisited edges one by one
        building an Euler circuit along the way.

        Parameters:
            int vertex: vertex being currently visited
            int unvisitedEs: total number of unvisited edges so far
            Walk walk: Euler walk built so far

        Returns: True iff an Euler circuit has been found and False otherwise
        """
       
        walk.addVertex(vertex)
        
        if unvisitedEs == 0 and walk.isCircuit():
            return True
        
        for i in range(self.totalV):
            if self.unvisitedE[vertex][i] >= 1:
                self.unvisitedE[vertex][i] -= 1
                self.unvisitedE[i][vertex] -= 1
                if self.tryVisiting(i, unvisitedEs - 1, walk):
                    return True
                else:
                    self.unvisitedE[vertex][i] += 1
                    self.unvisitedE[i][vertex] += 1

        walk.removeLastVertex()
        return False
