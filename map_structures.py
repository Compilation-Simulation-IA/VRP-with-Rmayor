from math import sqrt, pi, e
from typing import List
from agents import Authority
from storage import  Stop, Warehouse
import numpy as np
import networkx as nx
import random

class Graph:
    def __init__(self):
        self.graph = nx.Graph()  # Crear un grafo vacío 
        self.nodes = []  # Lista de nodos del grafo
        self.edges = []  # Lista de aristas del grafo
    
    def __repr__(self) -> str:
        return f"<Graph: Nodes Number: {len(self.nodes)}, Edges Number: {len(self.edges)}>"
    
    def add_node(self, node: Node):
        self.nodes.append(node)
        self.graph.add_node(node.ID, location=node.location)
    
    def add_edge(self, start: Node, end: Node, cost: float):
        self.edges.append(Edge(start, end, cost))
        self.graph.add_edge(start.ID, end.ID, weight=cost)
    
    def get_neighbors(self, node: Node) -> List[Node]:
        neighbors = []
        for neighbor in self.graph.neighbors(node.ID):  # Obtener vecinos del nodo a través del grafo
            neighbors.append(self.get_node_by_ID(neighbor))
        return neighbors
    
    def get_node_by_ID(self, ID: int) -> Node:
        for node in self.nodes:
            if node.ID == ID:
                return node
        return None  # Si no se encuentra el nodo, devolver None

class Node:
    """Nodos del grafo. La variable value puede ser un Stop, Warehouse o 
    simplemente una parada vacia(no tiene que recoger a nadie)"""

    def __init__(self, ID: int, value: Union[None, Stop, Warehouse], edges: List[Edge], location: Tuple[float, float]):
        self.ID = ID  # Identificador único del nodo
        self.location = location  # Tupla con las coordenadas (latitud, longitud) de la ubicación del nodo
        self.value = value
        self.edges = edges #TERMINAR, COMO SABER LAS ARISTAS DE UNA INSTANCIA DE NODE??

    def __repr__(self) -> str:
        return f"<Node: ID: {self.ID}, Value: {self.value}, Location: {self.location}>"

class Edge:
    def __init__(self, start: Node, end: Node, cost: float,  authorities: List[Authority]):
        self.start = start  # Nodo de inicio de la arista
        self.end = end  # Nodo de fin de la arista
        self.cost = cost  # Costo de recorrer la arista
        self.authorities = authorities  # Lista de autoridades que controlan la arista
        # Puede estar vacio.
    
    def __repr__(self) -> str:
        return f"<Edge: Start {self.start}, End: {self.end}>"
        

class Distribution_Type: 
    """ Clase para guardar todas las distribuciones que siguen las variables del problema"""
    def __init__(self):
        pass

    def generateExponential(self, lambda_value):
        return -(lambda_value * math.log(random.random()))
    
    def generateUniform(self, a, b):
        if a <= b :
            return random.uniform(a,b)
        raise Exception("Invalid argument.")