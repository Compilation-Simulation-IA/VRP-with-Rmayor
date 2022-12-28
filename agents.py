import random
from typing import List, Tuple
from storage import Route, Warehouse, Node, Edge

class Vehicle:
    wait = 0
    """Representa los vehículos de la compañía"""
    percent_of_deterioration_per_model = {"Lada": 5, "Moskovich": 7,"Ford": 5, "Mercedes Venz":3}

    def __init__(self, ID: int, model: str, current_location: Node, available: bool, capacity: int, clients_on_board: int, initial_miles: float, std_dev: float):
        self.ID = ID
        self.model = model # modelo del vehículo
        self.current_location = current_location
        self.available = available
        self.capacity = capacity
        self.initial_miles = initial_miles
        self.miles_traveled = 0
        self.std_dev = std_dev   # Desviación estándar inicial del vehículo
        self.spent = 0
        self.route = None
        self.clients_on_board = 0

    def __repr__(self) -> str:
        return f"<Vehicle: ID {self.ID}, Model: {self.model}, Capacity: {self.capacity},>" 

    def move(self, destination: Node):
        """Mueve al vehículo a su próximo destino"""
        self.current_location = destination
    
    def maintenance(self, time: int):
        """Le proporciona mantenimiento al vehiculo y disminuye el valor de millas_inicial en 
        dependencia del valor que devuelve la Gaussiana. Con esto se simula el deterioro del mismo."""
        self.available = False
        self.initial_miles -= random.gauss(0, self.std_dev)
        self.miles_traveled = 0
        #poner un Sleep donde el vehiculo se queda en manteniemiento
        self.spent += 100 # Aumenta el gasto acumulado en mantenimientos del vehículo
        self.available = True
        #f"Tarea de mantenimiento programada para {time} días. Valor actual de millas inicial: {self.millas_inicial}. Gasto acumulado: {self.gasto}"
        
    def assign_route(self, route: Route) -> bool:
        """Asigna un vehiculo a la ruta"""
        if self.route is None:
            self.route = route
            return True
        return False
        
    def unassign_route(self, route: Route) -> bool:
        """Elimina un vehiculo de la ruta"""
        if self.route is not None:
            self.route = None
            return True
        return False
    
    # Devuelve la cantidad de clientes que pudo recoger en esa parada
    def pick_up_clients(self) -> int:
        """Modifica la cantidad de clientes que quedan en la parada y la
         capacidad disponible en el vehículo"""
        result = min(self.capacity - self.clients_on_board, self.current_location.total_client)
        self.clients_on_board += result
        return result
    
    def drop_off_clients(self) -> int:
        result = self.clients_on_board
        self.clients_on_board = 0
        return result


class Authority:
    """Representa la autoridad del trafico """
    def __init__(self, ID: int, position: Edge, probability: float):
        self.ID = ID
        self.position = position
        self.probability = probability  # Probabilidad de que la autoridad para al vehículo
        
    def __repr__(self) -> str:
        return f"<Authority: ID {self.ID}, Position: {self.position}>"
    
    def stop_vehicle(self) -> bool:
        """Calcula la probabilidad de que la autoridad pare al vehículo y 
        devuelve True o False."""
        return random.random() < self.probability  # Devuelve True si el número aleatorio generado es menor que la probabilidad

class Company:
    """Representa la compañia de transporte"""
    def __init__(self, name: str, budget: float):
        self.name = name
        self.warehouses = []  #lista de almacenes
        self.routes = [] # lista de rutas de la empresa
        self.budget = budget # presupuesto disponible
        self.vehicles=[] #lista de vehiculos q tiene la compañia
        self.authorities = []  # Lista de autoridades que pueden parar a los vehículos
        self.in_maintenance = []

    def __repr__(self) -> str:
        return f"<Company: {self.name}>"

    def add_warehouse(self, warehouse: Warehouse):
        self.warehouses.append(warehouse)
        
    def remove_warehouse(self, warehouse: Warehouse):
        self.warehouses.remove(warehouse)
        
    def add_route(self, route: Route):
        self.routes.append(route)
        
    def remove_route(self, route: Route):
        self.routes.remove(route)
    
    # Añadir una parada a la ruta especificada
    def insert_stop(self, route: Route, stop: Node): 
        route.add_stop(stop)
        
    def relocate_stop(self, stop: Node, from_route: Route, to_route: Route):
        from_route.remove_stop(stop)
        to_route.add_stop(stop)
    
    def swap_stops(self, stop1: Node, route1: Route, stop2: Node, route2: Route):
        route1.stops[route1.stops.index(stop1)] = stop2
        route2.stops[route2.stops.index(stop2)] = stop1
        
    def replace_vehicle(self, old_vehicle: Vehicle, new_vehicle: Vehicle, route: Route):
        route.unassign_vehicle(old_vehicle)
        route.assign_vehicle(new_vehicle)
    
    def buy_vehicle(self, new_vehicle: Vehicle, cost: int):
        self.vehicles.append(new_vehicle)
        self.budget -= cost
    
    def delete_vehicle(self, old_vehicle: Vehicle, cost: int):
        self.vehicles.remove(old_vehicle)
        self.budget +=cost
    
    def assign_vehicles_to_route(self, route: Route, vehicles: List[Vehicle]): #QUITAR
        for v in vehicles:
            route.assign_vehicle(v)
    
    def unassign_vehicle_from_route(self, route: Route, vehicles: List[Vehicle]):
        for v in vehicles:
            route.unassign_vehicle(v)

    def check_vehicules(self): # PROPUESTA: QUE CHEQUEE UN VEHICULO A LA VEZ Y NO TODOS
        """Determina si cada vehículo debe ir al mantenimiento o no."""
        for vehicle in self.vehicles:
            if vehicle.millas_recorridas >= vehicle.millas_inicial:
                # El vehículo debe ir al mantenimiento
                vehicle.maintenance()
                self.in_maintenance.append(vehicle)
            elif vehicle.available:
                self.in_maintenance.remove(vehicle)
                # El vehículo no necesita mantenimiento todavía o  ya salio del mantenimiento

    def add_clients(self, clients: int, stop: Node):
        for route in self.routes:
            if stop in route.stops:
                stop.value.add_client(clients)
            return # f"Cliente añadido con exito."
        raise Exception("La parada proporcionada no pertenece a ninguna ruta")
    
    def remove_clients(self, clients: int, stop: Node):
        for route in self.routes:
            if stop in route.stops:
                stop.value.remove_client(clients)
            return # f"Cliente añadido con exito."
        raise Exception("La parada proporcionada no pertenece a ninguna ruta")

    def add_authority(self, authority: Authority, edge: Edge): 
        """Añade una autoridad que puede parar a los vehículos en una arista del grafo."""
        self.authorities.append(authority)
        edge.authorities.append(authority)
        

    def optimize_routes(self):
        # Iterar a través de todas las rutas y llevar a cabo operaciones de optimización 
        for route in self.routes:
            # Reubicar clientes para minimizar tiempo de espera en la parada
            # ...
            
            # Intercambiar clientes para minimizar tiempo de viaje total
            # ...
            
            # Cambiar vehículos para minimizar gasto de combustible
            # ...
            pass

