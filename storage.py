from typing import List
import math
from typing import List, Tuple, Optional, Union, Dict
import numpy as np
import networkx as nx
import random

""" Map Structures """

#class Stop:
#    """Representa las paradas donde se encuentran los clientes"""
#    def __init__(self, ID: int, total_client: int, location: Tuple[float, float], time_waiting: int):
#        self.id = ID
#        self.total_client = total_client
#        self.current_clients_in_stop = total_client #la cantidad de clientes que hay en la parada en ese momento. Tiene que ser menor que el total_client
#        self.time_waiting = time_waiting #time_waiting es en minutos
#        self.location = location
#
#    def __repr__(self) -> str:
#        return f"<Stop({self.id})>"
#    
#    def __str__(self) -> str:
#        return f"<Stop: ID: {self.id}, Location: {self.location}>"
#
#    def __gt__(self, other_stop):
#        return self.index > other_stop.index
#
#    def increase_wait(self, minutes):
#        self.time_waiting += minutes
#
#    def decrease_wait(self, minutes):
#        self.time_waiting = max(self.time_waiting - minutes, 0)
#
#    def add_client(self, drop: bool, client: Optional[int] = None):
#        """Si pick=True es que el vehiculo recoge a los clientes. Disminuye la cantidad de personas en la
#        parada, pero se mantiene igual el total que habian aqui. Este valor se usara cuando el vehuiculo
#        tenga que dejar a los clientes en sus paradas, saber cuantos soltar por cada una."""
#        if client is None:
#            if drop:  
#                self.current_clients_in_stop += 1
#            else: 
#                self.total_client += 1
#        else:
#            if drop:
#                self.current_clients_in_stop += client
#            else: 
#                self.total_client += client
#    
#    def remove_client(self, pick: bool, client: Optional[int] = None):
#        if client is None:
#            if pick: 
#                self.current_clients_in_stop -= 1
#            else:
#                self.total_client -= 1
#        else:
#            if pick:
#                self.current_clients_in_stop = min(0, self.current_clients_in_stop - client)
#            else:
#                self.total_client = min(0, self.total_client - client)
#

#class Warehouse:
#    """Representa un almacén o depósito central."""
#    def __init__(self, ID: int, location: Tuple[float, float]):
#        self.id = ID
#        self.location = location
#    
#    def __repr__(self) -> str:
#        return f"<Warehouse({self.id})>"
#
#    def __str__(self) -> str:
#        return f"<Warehouse: ID: {self.id}, Location: {self.location}>"

class MapNode:
    """Representan los nodos del grafo."""
    def __init__(self, id, people, authority = None, semaphore = None):
        self.id =id
        self.people = people #Si people = 0 entonces no es parada
        self.authority = authority
        self.semaphore = semaphore
        
#class Distribution_Type: 
#    """ Clase para guardar todas las distribuciones que siguen las variables del problema"""
#    def __init__(self):
#        pass
#
#    def generateExponential(self, lambda_value):
#        return -(lambda_value * math.log(random.random()))
#    
#    def generateUniform(self, a, b):
#        if a <= b :
#            return random.uniform(a,b)
#        raise Exception("Invalid argument.")

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

    def next_stop(self, actual_stop: MapNode) -> Union[MapNode, None]:
        index = self.stops.index(actual_stop)
        if index == len(self.stops) - 1:
            return None
        return self.stops[index + 1]

    def add_stop(self, stop: MapNode, position: Optional[int] = None):
        """Añade una parada a la ruta en la posición indicada. Si no se especifica 
        la posición, se añade al final de la ruta."""
        if position is None:
            self.stops.append(stop)
        else:
            self.stops.insert(position, stop)

    def remove_stop(self, stop: MapNode):
        """Elimina una parada de la ruta."""
        self.stops.remove(stop)

    def swap_stops(self, stop1: MapNode, stop2: MapNode):
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


