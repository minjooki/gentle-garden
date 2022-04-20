from cmu_112_graphics import *

# Dijkstra pseudocode start
# from https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf
# psuedocode also from wikipedia https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm 


# EX. weighted graph structure (from 110 graphs l
# ecture notes https://www.cs.cmu.edu/~15110/slides/week7-2-graphs.pdf)
# { A: [ [B,3],[C,4] ] , B: [ [A,3],[C,5] ] , C:[ [A,4],[B,5] ] }

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
    for drow in (-1,0,+1):
        for dcol in (-1,0,+1):
            if drow!=0 or dcol!=0:
                newRow = row + drow
                newCol = col + dcol
                if (newRow>=0 and newRow<len(board) and 
                    newCol>=0 and newCol<len(board[0])):
                    neighbors.append((newRow,newCol))
    return neighbors


def dijkstra(graph,start,target):
    notVisited = allNodesInGraph(graph) # all unvisited nodes (all at first)
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
                path.insert(vertex,0)
            path.insert(start,0)
            return path
        notVisited.remove(vertex) # remove from not visited

        for neighbor in notVisited: # check neighbor of curr node
            if isNeighbor(graph,vertex,neighbor):
                distanceToNode = distances[vertex]
                if distanceToNode==None:
                altPath = distanceToNode + getEdges(graph,vertex,neighbor)
                if altPath < distances[neighbor]: # if better path, update
                    distances[neighbor] = altPath
                    parentNodes[neighbor] = vertex
    return None

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
    if neighbor in graph[vertex]:
        return True
    return False

def getEdges(graph,vertex,neighbor):
    for otherNeighbor in graph[vertex]:
        if otherNeighbor[0]==neighbor:
            return otherNeighbor[1]