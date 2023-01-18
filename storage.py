from typing import List
import math
from typing import List, Tuple, Optional, Union, Dict
import numpy as np
import networkx as nx
import random

""" Map Structures """
class MapNode:
    """Representan los nodos del grafo."""
    def __init__(self, id, people, authority = None, semaphore = None):
        self.id =id
        self.people = people #Si people = 0 entonces no es parada
        self.authority = authority
        self.semaphore = semaphore

    def __repr__(self) -> str:
        return f"{self.id}"
    
    def __str__(self) -> str:
        pos = f'posición {self.id} del mapa'
        people = '' if self.people == 0 else f' que es una parada con {self.people} personas'
        authority = '' if self.authority == None else f' con autoridades'
        semaphore = '' if self.semaphore == None else f' con semáforo' 
        
        return pos + people  + authority + semaphore
        

    def __eq__(self, obj) -> bool:
        if self.id == obj.id:
            return True
        return False
    
    def copy(self):
        new_map_node = MapNode(self.id, self.people, self.authority, self.semaphore)
        return new_map_node

class Route:
    """Representa la ruta que sigue el vehiculo para recoger a los clientes y 
    llegar a su destino"""
    def __init__(self, ID: int, stops: List[MapNode]):
        self.id = ID
        self.actual_stop_index = 0
        self.stops = stops
        self.cost = 0 # Representa el costo de realizar la ruta

    def __repr__(self) -> str:
        """Representacion de la clase Route"""
        return f"<Route({self.id})>"

    def __str__(self) -> str:
        """Representacion de la clase Route"""
        return f"<Route: ID {self.id}, Stops Total Count: {len(self.stops)}>"

    #def next_stop(self, actual_stop: MapNode) -> Union[MapNode, None]:
    #    index = self.stops.index(actual_stop)
    #    if index == len(self.stops) - 1:
    #        return None
    #    return self.stops[index + 1]
#
    #def add_stop(self, stop: MapNode, position: Optional[int] = None):
    #    """Añade una parada a la ruta en la posición indicada. Si no se especifica 
    #    la posición, se añade al final de la ruta."""
    #    if position is None:
    #        self.stops.append(stop)
    #    else:
    #        self.stops.insert(position, stop)
#
    #def remove_stop(self, stop: MapNode):
    #    """Elimina una parada de la ruta."""
    #    self.stops.remove(stop)
#
    #def swap_stops(self, stop1: MapNode, stop2: MapNode):
    #    """Intercambia dos paradas de la ruta."""
    #    index1 = self.stops.index(stop1)
    #    index2 = self.stops.index(stop2)
    #    self.stops[index1], self.stops[index2] = self.stops[index2], self.stops[index1]
    #
    #def get_cost(self) -> float:
    #    """Calcula el costo total de la ruta."""
    #    self.cost = 0
    #    for stop in self.stops:
    #        self.cost += stop.value.cost
    #    return self.cost


