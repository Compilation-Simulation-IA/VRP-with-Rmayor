import random
from typing import List, Tuple, Dict
from storage import Route, MapNode
from enum import Enum
import networkx as nx
from ia.planning import Action,PlanningProblem

class Color(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3
class Vehicle:
    """Representa los vehículos de la compañía"""
    percent_of_deterioration_per_model = {"Lada": 5, "Moskovich": 7,"Ford": 5, "Mercedes Venz":3}

    def __init__(self, ID, capacity, initial_miles, risk_probability): #current_location: Dict, capacity: int, clients_on_board: int, initial_miles: float, std_dev: float, probability: float
        self.id = ID
        self.current_location = None
        self.days_off = 0 #disponibilidad del vehiculo. Si es > 0 representa los dias que no se usara
        self.capacity = capacity
        self.initial_miles = initial_miles
        #self.miles_traveled = 0
        #self.std_dev = std_dev   # Desviación estándar inicial del vehículo
        #self.spent = 0
        self.route = None
        #self.total_time_wait = 0
        self.people_on_board = 0
        self.risk_probability = risk_probability
        #self.pos_traffic_edge = -1
        #self.state = 0 
        self.speed = 0 #Representa los km/h
        #self.taxes = 0
        

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
        return f"<Vehicle({self.id})>" 
    
    def __str__(self):
        return f"<Vehicle: ID {self.id}>" #, Model: {self.model}>" 

    def move(self, origin, destination):
        """Mueve al vehículo a su próximo destino"""
        print('origin ' + str(origin))
        print('dest ' + str(destination))

        #self.miles_traveled += cost
        self.current_location = destination
        self.chage_speed()
    
    def chage_speed(self):
        self.speed = int(random.gauss(45, 10))        
    
    def pass_yellow(self) -> bool:
        """Calcula la probabilidad de que el vehiculo se pase o no la amarilla del semaforo.
        Devuelve True o False."""
        return random.random() < self.risk_probability
    
    #def maintenance(self, warehouse: Dict):
    #    """Le proporciona mantenimiento al vehiculo y disminuye el valor de millas_inicial en 
    #    dependencia del valor que devuelve la Gaussiana. Con esto se simula el deterioro del mismo."""
    #    self.days_off = 2
    #    self.current_location = warehouse
    #    self.initial_miles -= random.gauss(0, self.std_dev)
    #    self.miles_traveled = 0
    #    self.spent += 100 # Aumenta el gasto acumulado en mantenimientos del vehículo
    #    
    #    #f"Tarea de mantenimiento programada para {time} días. Valor actual de millas inicial: {self.millas_inicial}. Gasto acumulado: {self.gasto}"
        
    #def assign_route(self, route: Route) -> bool: #esto debe ir en compania
    #    """Asigna un vehiculo a la ruta"""
    #    if self.route is None:
    #        self.route = route
    #        return True
    #    return False
        
    #def unassign_route(self):
    #    """Elimina un vehiculo de la ruta"""
    #    self.route = None
    
    # Devuelve la cantidad de clientes que pudo recoger en esa parada
    def load(self, current_pos):
        """Modifica la cantidad de clientes que quedan en la parada y la
         capacidad disponible en el vehículo"""

        self.people_on_board += self.current_location.people
        self.current_location.people = 0
        
    
    def unload(self, current_pos):
        '''Descarga a los pasajeros en la posicion current_stop'''

        self.clients_on_board = 0

    def at_semaphore(self, current_pos: MapNode):
        wait = 0
        semaphore = current_pos.semaphore
        color = semaphore.state
            
        semaphore_time_left = sum(semaphore.color_range) - semaphore.time_color
        if color == Color.YELLOW:
            if self.pass_yellow():# no hace nada
                print(f"El {self} NO paró en la luz amarilla del {semaphore}.")
            else:
                wait = semaphore_time_left
                print(f"El {self} le cogio la luz amarilla en el {semaphore} y paró. Tiempo de espera: {wait}.")

        elif color == Color.RED:
            wait = semaphore_time_left
            print(f"El {self} le cogio la luz roja en el {semaphore}. Tiempo de espera: {semaphore_time_left}.")

        return wait

    def plan(self):
        '''Crea el problema de planificacion del vehiculo para la simulacion'''

        actions = [Action('move(v,x,y)',
                        precond='Adj(x,y) & At(v,x) & Empty(x) & FreePass(x)',
                        effect='~At(v,x) & At(v,y)',
                        domain='Vehicle(v) & Node(x) & Node(y)'),
                Action('load(v,x)',
                        precond='At(v,x) & ~Empty(x)',
                        effect='Empty(x)',
                        domain='Stop(x) & Vehicle(v)'),
                Action('unload(v,x)',
                        precond = 'At(v,x) & Empty(x)',
                        effect = '~Empty(x)',
                        domain= 'Vehicle(v) & End(x)'),
                Action('at_semaphore(v,x)',
                        precond='At(v,x) & Empty(x) & ~FreePass(x)',
                        effect= 'FreePass(x)',
                        domain='Vehicle(v) & Semaphore(x)'),                                    

                ]

        goals = f'~Empty({self.route[len(self.route)-1].id})'
        initial =f'At({self.id},{self.route[0].id})'
        domain = f'Vehicle({self.id}) & End({self.route[len(self.route)-1].id})'

        for i in range(len(self.route)):
                     
            if i < (len(self.route) - 1):
                initial += f' & Adj({self.route[i].id},{self.route[i+1].id})'

            if self.route[i].value > 0:
                initial += f' & ~Empty({self.route[i].id})'
                domain += f' & Stop({self.route[i].id}) & Node({self.route[i].id})'
            else:
                initial += f' & Empty({self.route[i].id})'
                domain += f' & Node({self.route[i].id})'

            if self.route[i].semaphore != None:
                initial += f' & ~FreePass({self.route[i].id})'
                domain += f' & Semaphore({self.route[i].id})'
            else:
                initial += f' & FreePass({self.route[i].id})'

            

        print('initial:' + initial)
        print('goals:' + goals)
        print('domain:' + domain)

        return PlanningProblem(initial=initial, goals=goals, actions=actions, agent=self, domain=domain)

        
class Semaphore:
    """Representa los semaforos en el mapa"""

    def __init__(self, position):
        self.position =position
        self.state = Color.GREEN
        self.color_range = [random.randint(1,30), 3, random.randint(1,30)]
        self.time_color = 0
    
    def __repr__(self) -> str:
        return f"<Semaphore({self.position})>"
    
    def __str__(self) -> str:
        return f"<Semaphore: Position {self.position}, State: {self.state.name}>"
    
    def update_color(self):
        if self.time_color == sum(self.color_range) :
            self.time_color = 0
        else:
            self.time_color += 1

        if self.time_color < self.color_range[0]:
            self.state = Color.GREEN
        elif self.time_color >self.color_range[0] and self.time_color < self.color_range[0] + self.color_range[1]:
            self.state = Color.YELLOW
        else:
            self.state = Color.RED
            

        

class Authority:
    """Representa la autoridad del trafico """
    def __init__(self, ID, probability = 0):
        self.id = ID
        self.probability = probability  # Probabilidad de que la autoridad para al vehículo. Tiene que estar entre 0 y 1e
        
    def __repr__(self) -> str:
        return f"<Authority({self.id})>"
    
    def __str__(self) -> str:
        return f"<Authority: ID {self.id}>"
    
    def __eq__(self, o) -> bool:
        return self.id == o.id
    
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
        
    def stop_vehicle(self, vehicle: Vehicle) -> int:
        """Detiene al vehiculo para ponerle una multa si excede la velocidad. El vehiculo continua su ruta."""
        if vehicle.speed > 60:
            vehicle.taxes += 50 # pone multa y continua
            return 1
        elif random.random() < self.probability: # Calcula la probabilidad de que la autoridad pare al vehículo y lo desvie del camino
            return 2 #devia el vehicle
        else:
            return 0 # no hace nada
            

class Company:
    """Representa la compañia de transporte"""
    def __init__(self, name: str, budget: float):
        self.name = name
        #self.warehouses = []  #lista de almacenes
        self.stops = {} # diccionario de paradas por clientes. Para despues formar las rutas
        self.routes = {} #a cada vehiculo se le asigna una ruta
        self.budget = budget # presupuesto disponible
        self.vehicles=[] #lista de vehiculos q tiene la compañia
        #self.authorities = []  # Lista de autoridades que pueden parar a los vehículos

    def __repr__(self) -> str:
        return f"<Company: {self.name}>"
    
    def __str__(self) -> str:
        return f"<Company: {self.name}>"

    def assign_vehicle_to_client(self):
        pass

    def assign_routes_to_vehicles(self):
        pass

    def start_route(self,vehicle, route):
        return vehicle.plan()
        
    def calculate_optimal_routes(self):
        """Este metodo llama a la IA para q me de la organizacion de los vehiculos por clientes y sus rutas"""
        pass
        
        
    # Añadir una parada a la ruta especificada
    #def insert_stop(self, route: Route, stop: MapNode): 
    #    route.add_stop(stop)
    #    
    #def relocate_stop(self, stop: MapNode, from_route: Route, to_route: Route):
    #    from_route.remove_stop(stop)
    #    to_route.add_stop(stop)
    #
    #def swap_stops(self, stop1: MapNode, route1: Route, stop2: MapNode, route2: Route):
    #    route1.stops[route1.stops.index(stop1)] = stop2
    #    route2.stops[route2.stops.index(stop2)] = stop1
    #    
    #def replace_vehicle(self, old_vehicle: Vehicle, new_vehicle: Vehicle, route: Route):
    #    route.unassign_vehicle(old_vehicle)
    #    route.assign_vehicle(new_vehicle)
    
    def buy_vehicle(self, new_vehicle: Vehicle, cost: int):
        self.vehicles.append(new_vehicle)
        self.budget -= cost
    
    #def delete_vehicle(self, old_vehicle: Vehicle, cost: int):
    #    self.vehicles.remove(old_vehicle)
    #    self.budget += cost

    def pay_taxes(self) -> int:
        result = 0
        for v in self.vehicles:
            result += v.taxes
            v.taxes = 0
        self.budget -= result
        return result


    #def check_vehicules(self): # PROPUESTA: QUE CHEQUEE UN VEHICULO A LA VEZ Y NO TODOS
    #    """Determina si cada vehículo debe ir al mantenimiento o no."""
    #    for vehicle in self.vehicles:
    #        if vehicle.millas_recorridas >= vehicle.millas_inicial:
    #            # El vehículo debe ir al mantenimiento
    #            vehicle.maintenance()
    #            vehicle.days_off = 2
    #            self.in_maintenance.append(vehicle)
    #        elif vehicle.days_off == 0:
    #            self.in_maintenance.remove(vehicle)
    #            # El vehículo no necesita mantenimiento todavía o  ya salio del mantenimiento
    
    def check_vehicle(self, vehicle: Vehicle):
        if vehicle.miles_traveled >= vehicle.initial_miles:
            # El vehículo debe ir al mantenimiento
            vehicle.days_off = random.randint(1,3)
        return vehicle.days_off
        

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

    def plan(self, assignations):

        plans=[]

        for v,r in assignations:

            new_plan = PlanningProblem(initial = f'~Done({v},{r}) & ~Checked({v}) & ~Payed({v})',
                                        goals = f'Checked({v})',
                                        actions = [Action('start_route(v,r)',
                                                            precond='~Done(v,r) & ~Checked(v) & ~Payed(v)',
                                                            effect='Done(v,r) & EndRoute(v)',
                                                            domain='Vehicle(v) & Route(r)'),
                                                    Action('check_vehicle(v)',
                                                            precond='EndRoute(v) & Payed(v) & ~Checked(v)',
                                                            effect='Checked(v)',
                                                            domain='Vehicle(v)'),
                                                    Action('pay_taxes(v)',
                                                            precond='~Checked(v) & EndRoute(v) & ~Payed(v)',
                                                            effect='Payed(v)',
                                                            domain='Vehicle(v)')

                                                    ],
                                        agent=self,
                                        domain=f'Vehicle({v}) & Route({r})')
            plans.append(new_plan)

        return plans
        

             
            

        

