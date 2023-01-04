import random
from typing import List, Tuple, Dict
from storage import Route, Warehouse, Stop
from enum import Enum
import networkx as nx

class Color(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3
class Vehicle:
    wait = 0
    """Representa los vehículos de la compañía"""
    percent_of_deterioration_per_model = {"Lada": 5, "Moskovich": 7,"Ford": 5, "Mercedes Venz":3}

    def __init__(self, ID: int, model: str, current_location: Dict, capacity: int, clients_on_board: int, initial_miles: float, std_dev: float, probability: float):
        self.ID = ID
        self.model = model # modelo del vehículo
        self.current_location = current_location
        self.days_off = 0 #disponibilidad del vehiculo. Si es > 0 representa los dias que no se usara
        self.capacity = capacity
        self.initial_miles = initial_miles
        self.miles_traveled = 0
        self.std_dev = std_dev   # Desviación estándar inicial del vehículo
        self.spent = 0
        self.route = None
        self.total_time_wait = 0
        self.clients_on_board = 0
        self.probability = probability
        self.pos_traffic_edge = -1
        self.state = 0 
        self.speed = 0
        """ los estados son:
        0 : no hacer nada
        1 : el vehiculo esta en movimiento
        2 : el vehiculo esta cargando pasajeros
        3 : el vehiculo esta descargando pasajeros
        4 : el vehiculo esta en mantenimiento
        5 : el vehiculo esta detenido por una autoridad del trafico
        6 : el vehiculo esta volviendo para atras en la arista pq lo paro una autoridad.
        """

    def __repr__(self) -> str:
        return f"<Vehicle({self.ID})>" 
    
    def __str__(self):
        return f"<Vehicle: ID {self.ID}, Model: {self.model}>" 

    def move(self, destination: Dict, cost: float):
        """Mueve al vehículo a su próximo destino"""
        self.miles_traveled += cost
        self.current_location = destination
    
    def speed_up(self, count: int):
        pass
    
    def pass_red(self) -> bool:
        """Calcula la probabilidad de que el vehiculo se pase o no la roja del semaforo.
        Devuelve True o False."""
        return random.random() < self.probability
    
    def maintenance(self, warehouse: Dict):
        """Le proporciona mantenimiento al vehiculo y disminuye el valor de millas_inicial en 
        dependencia del valor que devuelve la Gaussiana. Con esto se simula el deterioro del mismo."""
        self.days_off = 2
        self.current_location = warehouse
        self.initial_miles -= random.gauss(0, self.std_dev)
        self.miles_traveled = 0
        self.spent += 100 # Aumenta el gasto acumulado en mantenimientos del vehículo
        
        #f"Tarea de mantenimiento programada para {time} días. Valor actual de millas inicial: {self.millas_inicial}. Gasto acumulado: {self.gasto}"
        
    def assign_route(self, route: Route) -> bool:
        """Asigna un vehiculo a la ruta"""
        if self.route is None:
            self.route = route
            return True
        return False
        
    def unassign_route(self):
        """Elimina un vehiculo de la ruta"""
        self.route = None
    
    # Devuelve la cantidad de clientes que pudo recoger en esa parada
    def pick_up_clients(self) -> int:
        """Modifica la cantidad de clientes que quedan en la parada y la
         capacidad disponible en el vehículo"""
        result = min(self.capacity - self.clients_on_board, self.current_location.current_clients_in_stop)
        self.clients_on_board += result
        self.current_location.remove_client(True, result)
        # return result* self.current_location.time_waiting
        return result
    
    def drop_off_clients(self) -> int:
        result = 0
        if isinstance(self.current_location, Warehouse): 
            self.clients_on_board = result = 0
        elif isinstance(self.current_location, Stop):
            self.clients_on_board -= self.current_location.total_client
            result = self.current_location.current_clients_in_stop = self.current_location.total_client
        return result

class Semaphore:
    """Representa los semaforos en el mapa"""
#<<<<<<< HEAD
#    def __init__(self, ID: int, location: Tuple[float, float], color_range: List[int]): # Cambiado por [int], daba un error
#=======
    def __init__(self, ID: int, color_range: List[int]): #location: Tuple[float, float],
#>>>>>>> origin/roxy_simulate
        self.ID =ID
        #self.location = location
        self.state = Color.GREEN
        self.color_range = color_range
    
    def __repr__(self) -> str:
        return f"<Semaphore({self.ID})>"
    
    def __str__(self) -> str:
        return f"<Semaphore: ID {self.ID}, State: {self.state.name}>"

    def get_color(self, global_time: int) -> Tuple[Color, int]: #(color, semaphore_time)
        i = 0
        diference = global_time
        while diference > 0:
            diference -= self.color_range[i % 3]
            if diference <=0:
                j = i + 1
                self.state = Color((i % 3) + 1)
                return (self.state, self.color_range[i % 3] - abs(diference))
            i += 1
        

class Authority:
    """Representa la autoridad del trafico """
    def __init__(self, ID: int, probability: float):
        self.ID = ID
        self.probability = probability  # Probabilidad de que la autoridad para al vehículo. Tiene que estar entre 0 y 1e
        
    def __repr__(self) -> str:
        return f"<Authority({self.ID})>"
    
    def __str__(self) -> str:
        return f"<Authority: ID {self.ID}>"
    
    def __eq__(self, o) -> bool:
        return self.ID == o.ID
    
    def change_place(self, graph):
        edges = graph.edges
        for place in list(edges.data('weight')):
            traffic_list = place[2]['traffic_authorities']
            if self in traffic_list:
                place[2]['traffic_authorities'].remove(self)
                break

        # Obtener los nodos de inicio y fin de la arista elegida
        start, end = list(edges)[random.randint(0, len(edges)-1)]
        # Añadir la autoridad a la arista elegida aleatoriamente
        graph[start][end]['weight']['traffic_authorities'].append(self) #añadir +1 al costo de la arista por añadir una autoridad
        
    def stop_vehicle(self) -> bool:
        
        return random.random() < self.probability  # Devuelve True si el número aleatorio generado es menor que la probabilidad

    def turn_around_vehicle(self, vehicle: Vehicle) -> bool:
        """Calcula la probabilidad de que la autoridad pare al vehículo y lo desvie del camino."""
        pass
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
    
    def __str__(self) -> str:
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
    def insert_stop(self, route: Route, stop: Dict): 
        route.add_stop(stop)
        
    def relocate_stop(self, stop: Dict, from_route: Route, to_route: Route):
        from_route.remove_stop(stop)
        to_route.add_stop(stop)
    
    def swap_stops(self, stop1: Dict, route1: Route, stop2: Dict, route2: Route):
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
        self.budget += cost

    def check_vehicules(self): # PROPUESTA: QUE CHEQUEE UN VEHICULO A LA VEZ Y NO TODOS
        """Determina si cada vehículo debe ir al mantenimiento o no."""
        for vehicle in self.vehicles:
            if vehicle.millas_recorridas >= vehicle.millas_inicial:
                # El vehículo debe ir al mantenimiento
                vehicle.maintenance()
                vehicle.days_off = 2
                self.in_maintenance.append(vehicle)
            elif vehicle.days_off == 0:
                self.in_maintenance.remove(vehicle)
                # El vehículo no necesita mantenimiento todavía o  ya salio del mantenimiento
    
    def check_vehicle(self, vehicle: Vehicle):
        if vehicle.miles_traveled >= vehicle.initial_miles:
            # El vehículo debe ir al mantenimiento
            select_warehouse = random.randint(0, len(self.warehouses) - 1)
            vehicle.maintenance(self.warehouses[select_warehouse])# al vehiculo se le dara mantenimeinto en el warehouse escogido
            vehicle.state = 4
            vehicle.wait = vehicle.total_time_wait = 10 # espera 10 unidades de tiempo

            self.in_maintenance.append(vehicle)
        elif vehicle.days_off == 0 and vehicle in self.in_maintenance:
            self.in_maintenance.remove(vehicle)

    def add_clients(self, clients: int, stop: Dict):
        for route in self.routes:
            if stop in route.stops:
                stop.value.add_client(clients)
            return # f"Cliente añadido con exito."
        raise Exception("La parada proporcionada no pertenece a ninguna ruta")
    
    def remove_clients(self, clients: int, stop: Dict):
        for route in self.routes:
            if stop in route.stops:
                stop.value.remove_client(clients)
            return # f"Cliente añadido con exito."
        raise Exception("La parada proporcionada no pertenece a ninguna ruta")

    def add_authority(self, authority: Authority, edge: Dict): 
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

