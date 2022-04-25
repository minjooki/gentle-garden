from cmu_112_graphics import *

# Dijkstra pseudocode start
# from https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf
# psuedocode also from wikipedia https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm 


# EX. weighted graph structure (from 110 graphs l
# ecture notes https://www.cs.cmu.edu/~15110/slides/week7-2-graphs.pdf)
# { A: [ [B,3],[C,4] ] , B: [ [A,3],[C,5] ] , C:[ [A,4],[B,5] ] }

# stamina edges across different terrains go towards the smaller val
# stamina assignments:
#       grass = 5
#       plant = 7
#       tree = 9
#   any planted plot = 12

def makeGraphFromBoard(board):
    graph = {}
    rows = len(board)
    cols = len(board[0])

    for row in range(rows):
        for col in range(cols):
            graph[(row,col)] = getNeighbors(board,row,col)
    return graph

def getNeighbors(board,row,col):
    neighbors = []
    for (drow,dcol) in [(-1,0),(+1,0),(0,-1),(0,+1)]:
        newRow = row + drow
        newCol = col + dcol
        if (newRow>=0 and newRow<len(board) and 
            newCol>=0 and newCol<len(board[0])):
            neighborPair = []
            if board[newRow][newCol]==0:
                # grass
                neighborPair.append((newRow,newCol))
                neighborPair.append(5)
            elif board[newRow][newCol] in {2,4}:
                # plant
                neighborPair.append((newRow,newCol))
                neighborPair.append(7)
            elif board[newRow][newCol] in {1,3}:
                # tree
                neighborPair.append((newRow,newCol))
                neighborPair.append(9)
            elif board[newRow][newCol] in {5,50,51,52,53,54,55,56,6,60,
                                    61,62,63,64,65,66,99,100,101,'apple',
                                    'peach','lemon','strawb','tomato','blackb'}:
                # plant area
                neighborPair.append((newRow,newCol))
                neighborPair.append(12)
            neighbors.append(neighborPair)
                        
    return neighbors


def dijkstra(graph,start,target):
    notVisited = allNodesInGraph(graph) # all unvisited nodes (all at first)
    visited = set()
    distances = {start:0} # maps distance from source to vertex
    parentNodes = {} # maps vertex to its parent node in the path

    for node in notVisited: # initialize all nodes and distances
        if node != start:
            distances[node] = None

    while notVisited != set(): # repeat until all nodes visited
        # best vertex that has not been visited
        vertex = findMinDistance(notVisited,distances)

        if vertex == target: # if target, return path
            path = []
            while vertex != start: # while vertex is still defined
                parent = parentNodes[vertex]
                path.insert(0,parent)
                vertex = parent
            path.insert(0,start)
            return path

        notVisited.remove(vertex) # remove from not visited
        visited.add(vertex)

        for possibleNeighbor in notVisited: # check neighbor of curr node
            if isNeighbor(graph,vertex,possibleNeighbor):
                neighbor = possibleNeighbor
                distanceToCurrNode = distances[vertex]
                altPath = distanceToCurrNode + getEdges(graph,vertex,neighbor)
                if distances[neighbor]==None or altPath < distances[neighbor]: 
                    # if better path, update
                    distances[neighbor] = altPath
                    parentNodes[neighbor] = vertex
        

def allNodesInGraph(graph):
    # make a set of all the nodes in a graph
    allNodes = set()
    for node in graph:
        allNodes.add(node)
    return allNodes

def findMinDistance(notVisited,distances):
    # find the min distance/best node in not visited
    minDistance = None
    minNode = None
    for node in notVisited:
        if minDistance==None:
            minDistance = distances[node]
            minNode = node
        elif distances[node]!=None and distances[node]<minDistance:
            minDistance = distances[node]
            minNode = node
    return minNode

def isNeighbor(graph,vertex,neighbor):
    # is neighbor a real neighbor of vertex
    neighborList = graph[vertex]
    for pair in neighborList:
        if pair[0]==neighbor:
            return True
    return False

def getEdges(graph,vertex,neighbor):
    for neighborPair in graph[vertex]:
        if neighborPair[0]==neighbor:
            return neighborPair[1]