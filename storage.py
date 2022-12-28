from typing import List
from math import sqrt, pi, e
from typing import List, Tuple, Optional, Union
import numpy as np
import networkx as nx
import random

"""Map Structures"""

class Stop:
    """Representa las paradas donde se encuentran los clientes"""
    def __init__(self, ID: int, total_client: int, location: Tuple[float, float], time_waiting: int):
        self.ID = ID
        self.total_client = total_client
        self.time_waiting = time_waiting #time_waiting es en minutos
        self.location = location

    def __repr__(self) -> str:
        return f"<Stop: ID: {self.id}, Location: {self.location}>"

    def __gt__(self, other_stop):
        return self.index > other_stop.index

    def increase_wait(self, minutes):
        self.time_waiting += minutes

    def decrease_wait(self, minutes):
        self.time_waiting = max(self.time_waiting - minutes, 0)

    def add_client(self, client: Optional[int] = None):
        if client is None:
            self.total_client += 1
        else:
            self.total_client += client
    
    def remove_client(self, client: Optional[int] = None):
        if client is None:
            self.total_client -= 1
        else:
            self.total_client = min(0, self.total_client - client)


class Warehouse:
    """Representa un almacén o depósito central."""
    def __init__(self, ID: int, location: Tuple[float, float] ):
        self.ID = ID
        self.location = location
    
    def __repr__(self) -> str:
        return f"<Warehouse: ID: {self.ID}, Location: {self.location}, Vehicles Number: {len(self.vehicles)}>"
        
class Node:
    """Nodos del grafo. La variable value puede ser un Stop, Warehouse o 
    simplemente una parada vacia(no tiene que recoger a nadie)"""

    def __init__(self, ID: int, value: Union[None, Stop, Warehouse], location: Tuple[float, float]):
        self.ID = ID  # Identificador único del nodo
        self.location = location  # Tupla con las coordenadas (latitud, longitud) de la ubicación del nodo
        self.value = value

    def __repr__(self) -> str:
        return f"<Node: ID: {self.ID}, Value: {self.value}, Location: {self.location}>"

class Edge:
    def __init__(self, start: Node, end: Node, cost: float):
        self.start = start  # Nodo de inicio de la arista
        self.end = end  # Nodo de fin de la arista
        self.cost = cost  # Costo de recorrer la arista
        # Puede estar vacio.
    
    def __repr__(self) -> str:
        return f"<Edge: Start {self.start}, End: {self.end}>"


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

class Route:
    """Representa la ruta que sigue el vehiculo para recoger a los clientes y 
    llegar a su destino"""
    def __init__(self, ID: int, stops: List[Node]):
        self.ID = ID
        self.stops = []
        self.cost = 0 # Representa el costo de realizar la ruta

    def __repr__(self) -> str:
        """Representacion de la clase Route"""
        return f"<Route: ID {self.ID}, Stops Total Count: {len(self.stops)}>"

    def next_stop(self, actual_stop: Node) -> Union[Node,None]:
        index = self.stops.index(actual_stop)
        if index == len(self.stops) - 1:
            return Node
        return self.stops[index + 1]

    def add_stop(self, stop: Node, position: Optional[int] = None):
        """Añade una parada a la ruta en la posición indicada. Si no se especifica 
        la posición, se añade al final de la ruta."""
        if position is None:
            self.stops.append(stop)
        else:
            self.stops.insert(position, stop)

    def remove_stop(self, stop: Stop):
        """Elimina una parada de la ruta."""
        self.stops.remove(stop)

    def swap_stops(self, stop1: Stop, stop2: Stop):
        """Intercambia dos paradas de la ruta."""
        index1 = self.stops.index(stop1)
        index2 = self.stops.index(stop2)
        self.stops[index1], self.stops[index2] = self.stops[index2], self.stops[index1]
    
    def get_cost(self) -> float:
        """Calcula el costo total de la ruta."""
        self.cost = 0
        for stop in self.stops:
            self.cost += stop.value.cost
        return self.cost


