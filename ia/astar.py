import networkx as nx
from queue import PriorityQueue

def best_first_search(graph: nx.Graph, f):
    "Search nodes with minimum f(node) value first."
    node = problem.initial
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in graph.neighbors(node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return None