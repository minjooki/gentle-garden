from cmu_112_graphics import *

# Dijkstra pseudocode start
# from https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf

def dijkstra(start,target):
    notVisited = []
    graph = {}
    for node in notVisited:
        if node == start:
            graph[node] = 0