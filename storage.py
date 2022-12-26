from map_structures import Node
from agents import Client,  Vehicle
from typing import List

class Route:
    """Representa la ruta que sigue el vehiculo para recoger a los clientes y 
    llegar a su destino"""
    def __init__(self, ID: int, stops: List[Node], vehicles: List[Vehicle], cost: int):
        self.ID = ID
        self.vehicles = vehicles
        self.stops = []
        self.cost = cost # Representa el costo de realizar la ruta
        if self.check_stops(stops):
            self.stops = stops
        else:
            raise Exception("La lista de paradas es incorrecta. Solo se aceptan nodos de tipo Stop.")
        
    def __repr__(self) -> str:
        """Representacion de la clase Route"""
        return f"<Route: ID {self.ID}, Stops Total Count: {len(self.stops)}>"

    def check_stops(self, stops: List[Node]) -> bool:
        """Recorre la lista de stops y verifica que cada nodo tenga un atributo value de tipo Stop"""
        for stop in stops:
            if not isinstance(stop.value, Stop):
                return False
        return True

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
    
    def assign_vehicle(self, vehicle: Vehicle):
        """Asigna un vehiculo a la ruta"""
        self.vehicles.append(vehicle)
        
    def unassign_vehicle(self, vehicle: Vehicle):
        """Elimina un vehiculo de la ruta"""
        self.vehicles.remove(vehicle)
    
    def get_cost(self) -> float:
        """Calcula el costo total de la ruta."""
        cost = 0
        for stop in self.stops:
            cost += stop.value.cost
        return cost


class Stop:
    """Representa las paradas donde se encuentran los clientes"""
    def __init__(self, ID: int, location: Tuple[float, float], clients_list: List[Client], time_waiting: int):
        self.ID = ID
        self.clients_list = []
        if len(clients_list) != 0:
            for p in clients_list:
                self.add_person_to_stop(p)

        self.time_waiting = time_waiting #time_waiting es en minutos
        self.coordinates = (x_axis, y_axis)

    def __repr__(self) -> str:
        return f"<Stop: ID {self.id}:Coordinates {self.coordinates} in Route : {self.id_route}>"

    def __gt__(self, other_stop):
        return self.index > other_stop.index

    def increase_wait(self, minutes):
        self.time_waiting += minutes

    def decrease_wait(self, minutes):
        self.time_waiting = max(self.time_waiting - minutes, 0)

    def add_client(self, new_client):
        self.clients_list.append(new_client)
    
    def remove_client(self, old_client):
        self.clients_list.remove(old_client)


class Warehouse:
    """Representa un almacén o depósito central."""
    def __init__(self, ID: int, location: str, vehicles: List[Vehicle]):
        self.ID = ID
        self.location = location
        self.vehicles = vehicles
    
    def __repr__(self) -> str:
        return f"<Warehouse: ID: {self.ID}, Location: {self.location}, Vehicles Number: {len(self.vehicles)}>"
        
    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)
        
    def get_vehicle(self) -> Vehicle:
        # Devolver un vehículo disponible de la lista de vehículos del almacén
        for vehicle in self.vehicles:
            if vehicle.available:
                return vehicle
        return None
