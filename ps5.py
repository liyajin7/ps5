from itertools import product, combinations
from random import randint
from re import S
# from tkinter import N

'''
Before you start: Read the README and the Graph implementation below.
'''

class Graph:
    '''
    A graph data structure with number of nodes N, list of sets of edges, and a list of color labels.

    Nodes and colors are both 0-indexed.
    For a given node u, its edges are located at self.edges[u] and its color is self.color[u].
    '''

    # Initializes the number of nodes, sets of edges for each node, and colors
    def __init__(self, N, edges = None, colors = None):
        self.N = N
        self.edges = [set(lst) for lst in edges] if edges is not None else [set() for _ in range(N)]
        self.colors = [c for c in colors] if colors is not None else [None for _ in range(N)]
    
    # Adds a node to the end of the list
    # Returns resulting graph
    def add_node(self):
        self.N += 1
        self.edges.append(set())
        return self
    
    # Adds an undirected edge from u to v
    # Returns resulting graph
    def add_edge(self, u, v):
        assert(v not in self.edges[u])
        assert(u not in self.edges[v])
        self.edges[u].add(v)
        self.edges[v].add(u)
        return self

    # Removes the undirected edge from u to v
    # Returns resulting graph
    def remove_edge(self, u, v):
        assert(v in self.edges[u])
        assert(u in self.edges[v])
        self.edges[u].remove(v)
        self.edges[v].remove(u)
        return self

    # Resets all colors to None
    # Returns resulting graph
    def reset_colors(self):
        self.colors = [None for _ in range(self.N)]
        return self

    def clone(self):
        return Graph(self.N, self.edges, self.colors)

    def clone_and_merge(self, g2, g1u, g2v):
        '''
        DOES NOT COPY COLORS
        '''
        g1 = self
        edges = g1.edges + [[v + g1.N for v in u_list] for u_list in g2.edges]
        g = Graph(g1.N + g2.N, edges)
        if g1u is not None and g2v is not None:
            g = g.add_edge(g1u, g2v + g1.N)
        return g

    # Checks all colors
    def is_graph_coloring_valid(self):
        for u in range(self.N):
            for v in self.edges[u]:

                # Check if every one has a coloring
                if self.colors[u] is None or self.colors[v] is None:
                    return False

                # Make sure colors on each edge are different
                if self.colors[u] == self.colors[v]:
                    return False
        
        return True

'''
    Introduction: We've implemented exhaustive search for you below.

    You don't need to implement any extra code for this part.
'''

# Given an instance of the Graph class G, exhaustively search for a k-coloring
# Returns the coloring list if one exists, None otherwise.
def exhaustive_search_coloring(G, k=3):

    # Iterate through every possible coloring of nodes
    for coloring in product(range(0,k), repeat=G.N):
        G.colors = list(coloring)
        if G.is_graph_coloring_valid():
            return G.colors

    # If no valid coloring found, reset colors and return None
    G.reset_colors()
    return None


'''
    Part A: Implement two coloring via breadth-first search.

    Hint: You will need to adapt the given BFS pseudocode so that it works on all graphs,
    regardless of whether they are connected.

    When you're finished, check your work by running python3 -m ps5_color_tests 2.
'''

# Given an instance of the Graph class G and a subset of precolored nodes,
# Assigns precolored nodes to have color 2, and attempts to color the rest using colors 0 and 1.
# Precondition: Assumes that the precolored_nodes form an independent set.
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.
def bfs_2_coloring(G, precolored_nodes=None):
    # Assign every precolored node to have color 2
    # Initialize visited set to contain precolored nodes if they exist
    visited = set()
    G.reset_colors()
    preset_color = 2
    if precolored_nodes is not None:
        for node in precolored_nodes:
            G.colors[node] = preset_color
            visited.add(node)

        if len(precolored_nodes) == G.N:
            return G.colors

    # print(G.edges)

    # # initialize not-visited vertices
    # notVisited = []
    # for i in G.edges:
    #     if (i != visited[i]):
    #         notVisited.add(i)

    # while loop to restart BFS if not all vertices visited; accounts for graphs that aren't
    # connected
    while (len(visited) < G.N):

        # find arbitrary starting vertex
        s = 0
        while (s in visited):
            s = randint(0, G.N-1)

        # for neigh in G.edges[s]:
        #     G.colors[s] = 0
            
        #     if (G.colors[neigh] == 0):
        #         G.colors[s] = 1
        
        G.colors[s] = 0
        F = [s]

        # BFS for all graphs from single starting source
        while (len(F) > 0):

            # set current element to the first in the frontier
            curr = F.pop(0)
            # curr = F[0]
            # F = F.remove(curr)

            # print("\n\nNEW LOOP. curr = ", curr)
            
            # print("neighbors of curr: ", G.edges[curr])
            for neigh in G.edges[curr]:

                # if both vertices (curr and neighbor) are already visited and colored with same color,
                # then no 2-coloring: return None
                if (G.colors[curr] == G.colors[neigh]):
                    # print("IF LOOP: G.colors[curr] == G.colors[neigh]")
                    G.reset_colors()
                    return None

                # if neighbor hasn't been visited, color according to current node color
                if not (neigh in visited):
                    # print("IF LOOP: neighbor hasn't been visited")
                    G.colors[neigh] = 1 if (G.colors[curr] == 0) else 0

                    # add neighbor to front of frontier to be popped next
                    F.insert(0, neigh)

            # if not (curr in visited):
            visited.add(curr)


    if G.is_graph_coloring_valid():
        return G.colors
    else:
        G.reset_colors()
        return None


    #     # we have a frontier with all the indices of immediate visited
    #     # in here, find the minimum coloring for graph.
    #     for j in F:
    #         # for every vertex in the frontier, we need to apply two-coloring.
    #         pass

    #     # update frontier F to be V-S, visited to include F
    #     for i in G.edges[s]:
    #         if (visited.find(i) == -1):
    #             F.add(i)
    #             visited.add(i)

    #     # need to update s somewhere!
    #     # at the end, how do we preserve
    #     F = []
    
    # # remove visited from set of edges G
    # for node in G.edges:
    #     pass

    # # run BFS until you've finished this connected component
    # for node in G.edges:
    #     # iterate through each neighbor node in each edge
    #     for neighbor in node:
    #         # frontier here is the neighbors in node that are not already in visited

    # check whether there are still unvisited nodes: if so, pick arbitrary start vertex there
    # and run BFS again


'''
    Part B: Implement is_independent_set.
'''

# Given an instance of the Graph class G and a subset of precolored nodes,
# Checks if subset is an independent set in G 
def is_independent_set(G, subset):

    # for every vertex in the set
    for v in subset:
        # iterate through all its neighbors
        for neigh in G.edges[v]:

            # if any neighbor of a vertex in the set is also in the set, set is not independent
            if (neigh in subset):
                return False

    return True

'''
    Part C: Implement the 3-coloring algorithm from the sender receiver exercise.
    
    Make sure to call the bfs_2_coloring and is_independent_set functions that you already implemented!

    Hint 1: You will want to use the Python `combinations` function from the itertools library
    to enumerate all possible independent sets. Remember that each element of combinations is a tuple,
    so you may need to convert it to a list.

    Hint 2: Python itertools functions compute their results lazily, which means that they only
    calculate each element as the program requests it. This saves time and space, since it
    doesn't need to store the entire list of combinations up front. You should NOT try to convert the result
    of the entire combinations call to a list, since that will force Python to precompute everything.
    Instead, you should iterate over them in a for loop, which will maintain the lazy behavior we want.
    See the call to "product" in exhaustive_search for an example.

    When you're finished, check your work by running python3 -m ps5_color_tests 3.
    Don't worry if some of your tests time out: that is expected.
'''

# Given an instance of the Graph class G (which has a subset of precolored nodes), searches for a 3 coloring
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.
def iset_bfs_3_coloring(G):

    # see if graph is first 2-colorable
    attempt = bfs_2_coloring(G, [])
    if (attempt != None):
        return attempt

    # enumerate all possible independent sets of possible sizes at most n/3
    for size in range(G.N//3 + 1):
        
        # generate all possible subsets of size size
        possible_subsets = combinations(range(G.N), size)

        # check if each subset is iset
        for subset in possible_subsets:
            if is_independent_set(G, list(subset)):
                
                # according to Lemme 2.1, colors "subset" vertices as 2 (f_S), attempts to assign
                # 2-coloring to the rest of the vertices (f_{-S})
                coloring_attempt = bfs_2_coloring(G, list(subset))

                if (coloring_attempt != None):
                    return coloring_attempt

    # return None if no possible 3-coloring found
    return None

# Feel free to add miscellaneous tests below!
if __name__ == "__main__":
    G0 = Graph(2).add_edge(0, 1)
    print(bfs_2_coloring(G0))
    print(iset_bfs_3_coloring(G0))