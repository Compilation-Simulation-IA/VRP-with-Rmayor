from map_structures import Node, Edge
from storage import Route
from storage import Route, Warehouse
from typing import List

class Company:
    """Representa la compañia de transporte"""

    def __init__(self, name: str, warehouses: List[Warehouse], routes: List[Route], budget: float):
        self.name = name
        self.warehouses = warehouses  #lista de almacenes
        self.routes = routes # lista de rutas de la empresa
        self.budget = budget # presupuesto disponible
        self.vehicles=[] #lista de vehiculos q tiene la compañia
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
    
    
    #añadir una parada a la ruta especificada
    def insert_stop(self,id_route, location): #ARREGLAR
        self.routes[id_route].append(location)
 
        
    def relocate_stop(self, stop: Node, from_route: Route, to_route: Route):
        from_route.remove_stop(stop)
        to_route.add_stop(stop)
    
    def swap_stops(self, stop1: Node, route1: Route, stop2: Node, route2: Route):
        route1.stops[route1.stops.index(stop1)] = stop2
        route2.stops[route2.stops.index(stop2)] = stop1
        
    def replace_vehicle(self, old_vehicle: Vehicle, new_vehicle: Vehicle, route: Route):
        route.unassign_vehicle(old_vehicle)
        route.assign_vehicle(new_vehicle)
    
    def buy_vehicle(self, new_vehicle):
        self.vehicles.append(new_vehicle)
    
    def delete_vehicle(self, old_vehicle):
        self.vehicles.remove(old_vehicle)
    
    def assign_vehicles_to_route(self, route: Route, vehicles: List[Vehicle]):
        for v in vehicles:
            route.assign_vehicle(v)
    
    def unassign_vehicle_from_route(self, route: Route, vehicles: List[Vehicle]):
        for v in vehicles:
            route.unassign_vehicle(v)

    def check_vehicules(self):
        """Cada vez q un vehiculo termina su recorrido este se chequea para 
        determinar si se manda al mantenimiento no"""
        pass

    def send_to_maintenance(self, vehicule: Vehicle): 
        pass

    def add_clients(self, new_clients: List[Client], stop: Node):
        for route in self.routes:
            if stop in route.stops:
                for nc in new_clients:
                    stop.value.add_client(nc)
                return # f"Cliente añadido con exito."
        raise Exception("La parada proporcionada no pertenece a ninguna ruta")
    
    def remove_clients(self, old_clients: List[Client], stop: Node):
        for route in self.routes:
            if stop in route.stops:
                for oc in old_clients:
                    stop.value.remove_client(oc)
                return # f"Cliente añadido con exito."
        raise Exception("La parada proporcionada no pertenece a ninguna ruta")

    def add_route(self, route: Route):
        self.routes.append(route)

    def add_authority(self, authority: Authority, edge: Edge): #TERMINAR
        #stop_start = edge.start
        #for r in self.routes:
        #    if stop_start in r.stops:
        #        r.stops[r.stops.index(stop_start)].

        #self.authorities.append(location)
        pass

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



class Vehicle:
    """Representa los vehículos de la compañía"""
    percent_of_deterioration_per_model = {"Lada": 5, "Moskovich": 7,"Ford": 5, "Mercedes Venz":3}

    def __init__(self, ID: int, model: str, location: Node, destination: Node, available: bool, capacity: int, initial_miles: float, std_dev: float):
        self.ID = ID
        self.model = model # modelo del vehículo
        self.location = location
        self.destination = destination
        self.available = available
        self.capacity = capacity
        self.initial_miles = initial_miles
        self.miles_traveled = 0
        self.std_dev = std_dev #  # Desviación estándar inicial del vehículo
        self.spent = 0

    def __repr__(self) -> str:
        return f"<Vehicle: ID {self.ID}, Model: {self.model}, Capacity: {self.capacity},>" 

    def move(self):
        """Mueve al vehículo a su próximo destino"""
        self.location = self.destination
    
    def maintenance(self, time: int) -> str:
        """Le proporciona mantenimiento al vehiculo y disminuye el valor de millas_inicial en 
        dependencia del valor que devuelve la Gaussiana. Con esto se simula el deterioro del mismo."""
        if self.miles_traveled == self.initial_miles: 
            self.available = False
            self.initial_miles -= random.gauss(0, self.std_dev)
            self.miles_traveled = 0
            self.spent += 100 # Aumenta el gasto acumulado en mantenimientos del vehículo
            return  True #f"Tarea de mantenimiento programada para {time} días. Valor actual de millas inicial: {self.millas_inicial}. Gasto acumulado: {self.gasto}"
        
        return False #f"El vehiculo no necesita de mantenimiento"
    

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

class Client:
    """Representa los clientes que la compañía tiene que recoger"""
    def __init__(self, ID: int):
        self.ID = ID
       
    def __repr__(self):
        return f"<Client: ID {self.ID}>"