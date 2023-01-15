import random
from ia.ant_colony import AntColony
from ia.simulated_annealing import SimulatedAnnealingVehiclesToClients, SimulatedAnnealingRouteToVehicle
from enum import Enum
import networkx as nx
from ia.planning import Action,PlanningProblem
import ast
import numpy as np



class Color(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3
class Vehicle:
    """Representa los vehículos de la compañía"""
    percent_of_deterioration_per_model = {"Lada": 5, "Moskovich": 7,"Ford": 5, "Mercedes Venz":3}

    def __init__(self, ID, capacity, initial_miles, risk_probability, logger, map): #current_location: Dict, capacity: int, clients_on_board: int, initial_miles: float, std_dev: float, probability: float
        self.id = ID
        self.current_location = None
        self.days_off = 0 #disponibilidad del vehiculo. Si es > 0 representa los dias que no se usara
        self.capacity = capacity
        self.initial_miles = initial_miles
        self.miles_traveled = 0
        self.route = None
        self.people_on_board = 0
        self.risk_probability = risk_probability
        self.speed = 0 #Representa los km/h
        self.taxes = 0
        self.chage_speed()
        self.count_moves = 0 
        self.logger = logger
        self.initial = None # posicion inicial el deposito de la compania
        self.free_pass = False
        self.free_pass_authority = False
        self.map = map
        self.last_stop = None
        self.turning_back = False
        
        

    def __repr__(self) -> str:
        return f"<Vehicle({self.id})>" 
    
    def __str__(self):
        return f"<Vehicle: ID {self.id}>" #, Model: {self.model}>" 

    def move(self, origin, destination):
        """Mueve al vehículo a su próximo destino"""
        speed = self.speed
        #self.miles_traveled += cost
        self.chage_speed()
        self.count_moves += 1
        self.current_location = self.route[self.count_moves]
        self.logger.log(f"El {self} se desplazo de {origin} a {destination} con una velocidad {speed}.")

        return speed        
    
    def change_speed(self):
        self.speed = int(random.gauss(45, 10))        
    
    def pass_yellow(self) -> bool:
        """Calcula la probabilidad de que el vehiculo se pase o no la amarilla del semaforo.
        Devuelve True o False."""
        return random.random() < self.risk_probability
    
    
    # Devuelve la cantidad de clientes que pudo recoger en esa parada
    def load(self, current_pos):
        """Modifica la cantidad de clientes que quedan en la parada y la
         capacidad disponible en el vehículo"""

        
        # cambiar cantidad de personas en la parada en el mapa
        #               
        people = min(self.current_location.people, self.capacity - self.people_on_board)
        self.last_stop = self.current_location
        self.people_on_board += people
        self.current_location.people -= people 
        self.logger.log(f"El {self} cargo {people} personas en la parada {current_pos}.")


        if self.capacity == self.people_on_board:
            self.turning_back = True
            self.change_route()
        
        return people
        
    
    def unload(self, current_pos):
        '''Descarga a los pasajeros en la posicion current_stop'''

        people = self.people_on_board
        self.people_on_board = 0
        self.logger.log(f"El {self} descargo {people} personas en la parada {current_pos}.")
        return people

    def at_semaphore(self, current_pos):
        wait = 0
        semaphore = self.current_location.semaphore
        color = semaphore.state
            
        semaphore_time_left = sum(semaphore.color_range) - semaphore.time_color
        if color == Color.YELLOW:
            if self.pass_yellow():# no hace nada
                self.logger.log(f"El {self} NO paró en la luz amarilla del {semaphore}.")
            else:
                wait = semaphore_time_left
                self.logger.log(f"El {self} le cogio la luz amarilla en el {semaphore} y paró. Tiempo de espera: {wait}.")

        elif color == Color.RED:
            wait = semaphore_time_left
            self.logger.log(f"El {self} le cogio la luz roja en el {semaphore}. Tiempo de espera: {semaphore_time_left}.")
        
        else:
            self.logger.log(f"El {self} paso con luz verde en el {semaphore}.")

        return wait

    def at_authority(self, decision):
        if decision == 2:
            # cambiar ruta
            pass

    def change_route(self):
        pass

    def relocate_route(self, origin, routes):
       
        start = len(routes)
        stops = []     
             

        for i in range(len(routes)):
            if routes[i].id == origin:
                start = i
                print(start)
                stops.append(ast.literal_eval(routes[i].id))

            if i > start and routes[i].people > 0:
                stops.append(ast.literal_eval(routes[i].id))

        stops.append(ast.literal_eval(routes[len(routes)-1].id)) 

        origin= ast.literal_eval(origin)
        not_available = ast.literal_eval(routes[start+1].id)

        temp = self.graph_map[origin][not_available]['weight']
        self.graph_map[origin][not_available]['weight'] = float('inf')       

        
        path = self.company.get_complete_route(stops,self.graph_map)

        path = routes[0:start+1] + path   

        self.graph_map[origin][not_available]['weight']=temp

        return path
        
  
    def plan(self):

        if self.turning_back and self.current_location.id == self.last_stop.id and self.capacity != self.people_on_board:
            self.turning_back = False

        if self.current_location.authority != None and not self.free_pass_authority:
            self.free_pass_authority = True
            return 'at_authority()'
        elif (self.current_location.people > 0 and self.people_on_board != self.capacity and not self.turning_back) or (self.turning_back and self.current_location.people > 0 and self.people_on_board != self.capacity and self.current_location.id == self.last_stop.id):
            return 'load'
        elif self.current_location.id == self.route[len(self.route)-1] and self.people_on_board > 0:
            return 'unload'
        elif self.current_location.semaphore != None and not self.free_pass:
            return 'at_semaphore'        
        else:
            self.free_pass_authority = False
            self.free_pass = False
            return 'move'

        


    def goal_test(self):

        if self.current_location.id != self.route[len(self.route)-1].id:
            return False

        for node in self.route:
            if node.people > 0:
                return False

        return True
        

    def plan(self):
        '''Crea el problema de planificacion del vehiculo para la simulacion'''

        if self.current_location == None:
            self.current_location = self.route[0]

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
        initial =f'At({self.id},{self.current_location.id})'
        domain = f'Vehicle({self.id}) & End({self.route[len(self.route)-1].id})'

        for i in range(len(self.route)):
                     
            if i < (len(self.route) - 1):
                initial += f' & Adj({self.route[i].id},{self.route[i+1].id})'

            if self.route[i].people > 0:
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
    def __init__(self, ID , map = None, probability = 0.5):
        self.id = ID
        self.probability = probability  # Probabilidad de que la autoridad para al vehículo. Tiene que estar entre 0 y 1e
        self.map = map

    def __repr__(self) -> str:
        return f"<Authority({self.id})>"
    
    def __str__(self) -> str:
        return f"<Authority: ID {self.id}>"
    
    def __eq__(self, o) -> bool:
        if o == None:
            return False
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
        result = 0
        if vehicle.speed > 60:
            vehicle.logger.log(f"El {vehicle} fue multado por {self}, por ir a {vehicle.speed} km/h.")
            vehicle.taxes += 50 # pone multa y continua
            result = 1

        elif random.random() < self.probability: # Calcula la probabilidad de que la autoridad pare al vehículo y lo desvie del camino
            vehicle.logger.log(f"El {vehicle} fue desviado del camino por {self}.")
            route = vehicle.route
            next_stop = None
            start = len(route)
            path = None

            for i in range(len(route)):
                if self.id == route[i].id:
                    start = i
                if i > start and route[i].people > 0 or i == (len(route)-1):
                    next_stop = route[i].id
                    break
            
            origin = ast.literal_eval(self.id)
            dest =ast.literal_eval(next_stop)            

            if dest != ast.literal_eval(route[start+1].id):
                weight = self.map[origin][ast.literal_eval(route[start+1].id)]['weight']
                self.map.remove_edge(origin,ast.literal_eval(route[start+1].id))
                path = nx.shortest_path(self.map,origin,dest, weight='weight')
                self.map.add_edge(origin,ast.literal_eval(route[start+1].id),weight=weight)

            if path != None:
                result = 2 #devia el vehicle
        else:
            vehicle.logger.log(f"El {vehicle} no fue parado por {self}.")
        return result
            
class Company:
    """Representa la compañia de transporte"""

    def __init__(self, name: str, budget: float, map, clients, vehicles, depot, logger):
        self.name = name
        self.depot = depot # MapNode con la localizacion del deposito de la compania
        self.clients = clients # lista de diccionarios de la forma {client_name:[[MapNodes],MapNode]}
        self.routes = {} #a cada vehiculo se le asigna una ruta
        self.budget = budget # presupuesto disponible
        self.vehicles = vehicles # lista de vehiculos q tiene la compañia
        self.map = map
        self.vehicle_client = {}
        self.vehicle_stop = {}
        self.vehicle_route = []
        self.substitute = {}# diccionario de vehiculo que esta sustituyendo al que esta en mantenimiento
        # y era del cliente. La ruta que era original al vehiculo que se mando al mantenimiento
        self.available_vehicles = [] # vehiculos que no estan asignados a ningun 
        self.__assign()
        
        self.logger = logger

    def __repr__(self) -> str:
        return f"<Company: {self.name}>"
    
    def __str__(self) -> str:
        return f"<Company: {self.name}>"

    def __assign(self):

        self.__assign_vehicle_to_client()
        self.__assign_stops_to_all_vehicles()
        self.__check_assign_vehicles()

        self.__get_route_of_vehicles()


    def __check_assign_vehicles(self):

        not_assigned_vehicles = []

        for v in self.vehicle_stop.keys():
            if len(self.vehicle_stop[v]) == 2:
                not_assigned_vehicles.append(v)
        
        i = 0
        while i < len(not_assigned_vehicles):
            self.vehicle_stop.pop(not_assigned_vehicles[i])


        if len(not_assigned_vehicles) >0:
            for value in self.vehicle_client.values():
                for v in value:
                    if v.id in not_assigned_vehicles:
                        value.remove(v)



                    
    def __assign_stops_to_all_vehicles(self):

        for c in self.vehicle_client.keys():
            vehicles = self.vehicle_client[c]
            stops = self.clients[c][0] + [self.depot] + [self.clients[c][1]] 
            self.__assign_stops_to_vehicle(vehicles,stops)

    def __assign_stops_to_vehicle(self, vehicles, stops):

        """Asigna vehiculos a rutas de un cliente. 
        Retorna diccionario de la forma {vehiculo.id:[lista de paradas]}"""
        
        vehicle_capacities = [v.capacity for v in vehicles]
        client_demands = [s.people for s in stops]

        assignations, cost = SimulatedAnnealingRouteToVehicle(vehicle_capacities, client_demands).run()

        for i in range(len(assignations)):
            if assignations[i] == 1:
                vehicle = vehicles[int(i/len(stops))]
                stop = stops[i%len(stops)]
                
                if vehicle.id in self.vehicle_stop.keys():
                    self.vehicle_stop[vehicle.id].append(stop)
                else:
                    self.vehicle_stop.update({vehicle.id:[stop]})

    
    def __assign_vehicle_to_client(self):
        """Asigna a cada cliente los vehiculos 
        necesarios para recoger a todas las personas en las paradas. 
        Retorna diccionario de la forma {client_name:[lista vehiculos]}"""

        vehicles_capacities = []
        clients_demands = []
        
        for v in self.vehicles:
            vehicles_capacities.append(v.capacity)

        for c in self.clients.values():
            clients_demands.append(sum([m.people for m in c[0]]))            

        assignations, cost = SimulatedAnnealingVehiclesToClients(vehicles_capacities,clients_demands).run()
        
        for i in range(len(assignations)):
            if assignations[i] == 1:
                vehicle = self.vehicles[int(i/len(self.clients))]
                client = list(self.clients.keys())[i%len(self.clients)]
                
                if client in self.vehicle_client.keys():
                    self.vehicle_client[client].append(vehicle)
                else:
                    self.vehicle_client.update({client:[vehicle]})



    def __get_route_of_vehicles(self):

        for v in self.vehicle_stop.keys():
            distances = self.__get_distance_beetween_stops(self.vehicle_stop[v])
            route = AntColony(distances, 5, 100, 0.95, alpha=1, beta=1, delta_tau = 2).run()[0]
            route_nodes = []
            for x,y in route:
                route_nodes.append(self.vehicle_stop[v][x])
            route_nodes.append(self.vehicle_stop[v][len(self.vehicle_stop[v])-1])

            route_nodes = self.__get_complete_route(route_nodes)
            self.vehicle_route.update({v: self.get_vehicle_from_id(v),'R' + v:route_nodes})
     

    def __get_distance_beetween_stops(self, stops):
        
        distances = [[0 for i in range(len(stops))] for j in range(len(stops))]

        for i in range(len(stops)):
            for j in range(len(stops)):
                if i != j:
                    distances[i][j]=nx.shortest_path_length(self.map,source=ast.literal_eval(stops[i].id),target=ast.literal_eval(stops[j].id),weight='weight')
                else:
                    distances[i][j] = 0

        
        return np.array(distances)


    def __get_complete_route(self, stops):

        """Obtiene la ruta completa a partir de una secuencia de paradas"""

        path = []
        nodes = nx.get_node_attributes(self.map,'value')
        
        for i in range(len(stops)-1):
            shortest_path = nx.shortest_path(self.map,ast.literal_eval(stops[i].id),ast.literal_eval(stops[i+1].id),weight='weight')
            for j in range(len(shortest_path)):
                path.append(nodes[shortest_path[j]])

        return path

    def __get_vehicle_from_id(self, vehicle_id):
        """Devuelve el objeto vehiculo a partir de su id"""

        for a in self.assignations:
            if list(a.keys())[0] == str(vehicle_id):
                return list(a.values())[0]

    def start_route(self, vehicle_id, route_id):
        vehicle = self.__get_vehicle_from_id(vehicle_id)
        self.logger.log(f"{self}: El {vehicle} acaba de comenzar la ruta.")
        return vehicle.plan()

         
        
    def buy_vehicle(self, new_vehicle: Vehicle, cost: int):
        self.logger.log(f"{self} compro un nuevo {new_vehicle} a {cost} pesos.")
        self.vehicles.append(new_vehicle)
        self.budget -= cost
    
    def pay_taxes(self, vehicle_id) -> int: 
        """Paga las multas de los vehiculos en esa ruta si hubo y tambien cobra al cliente por haber
        pedido el servicio de taxis."""
        vehicle = self.__get_vehicle_from_id(vehicle_id)
        result = vehicle.taxes
        self.logger.log(f"{self} tuvo perdidas de {result} pesos en multas por el {vehicle}.")
        vehicle.taxes = 0
        income = 10 * vehicle.capacity * len(vehicle.route) # El pago por los servicios
        self.budget +=income
        self.logger.log(f"{self} tuvo ganancias de {income} pesos por los servivios prestados por el {vehicle}.")
        self.budget -= result
        return result

    def check_vehicle(self, vehicle_id):
        vehicle = self.__get_vehicle_from_id(vehicle_id)
        if vehicle.miles_traveled >= (3/4) * vehicle.initial_miles:
            vehicle.days_off = random.randint(1,3)
            self.find_replacement(vehicle)
            self.logger.log(f"El {vehicle} debe ir al mantenimiento por {vehicle.days_off}")
        else:
            self.logger.log(f"El {vehicle} esta en perfectas condiciones.")

        return vehicle.days_off        

    def find_replacement(self, vehicle: Vehicle):
        """Cuando un vehiculo se manda a mantenimiento buscar sustituto si se puede."""
        #Ver si hay vehiculos disponibles: Son los vehiculos que estan en self.vehicles que no estan
        # en self.vehicles_client:
        
        if len(self.available_vehicles) != 0:
            max_capacity = 0
            v_max = None
            for v in self.available_vehicles:
                if max_capacity < v.capacity:
                    v_max = v
                    max_capacity = v_max.capacity

            v_max.route = vehicle.route
            vehicle.route = []
            self.vehicle_route.remove(vehicle.id)
            self.vehicle_route[v_max] = v_max.route

            for c in self.vehicle_client.values():
                for i in c:
                    if vehicle.id == c[i]:
                        c.remove(vehicle.id)
                        c.append(v_max.id)
                        break
            
        # Ver si el cliente tiene asignado otros vehiculos


    def plan(self):

        plans=[]

        for a in self.vehicle_route:            
            v,r = a.keys()
            if v.days_off == 0:#ARREGLAR PQ V,R SON NOMBRES Y NO OBJETOS

                new_plan = PlanningProblem(initial = f'~Done({v},{r}) & ~Checked({v}) & ~Payed({v})',
                                            goals = f'Checked({v})',
                                            actions = [Action('start_route(c,v,r)',
                                                                precond='~Done(v,r) & ~Checked(v) & ~Payed(v)',
                                                                effect='Done(v,r) & EndRoute(v)',
                                                                domain='Vehicle(v) & Route(r) & Company(c)'),
                                                        Action('check_vehicle(c,v)',
                                                                precond='EndRoute(v) & Payed(v) & ~Checked(v)',
                                                                effect='Checked(v)',
                                                                domain='Vehicle(v) & Company(c)'),
                                                        Action('pay_taxes(c,v)',
                                                                precond='~Checked(v) & EndRoute(v) & ~Payed(v)',
                                                                effect='Payed(v)',
                                                                domain='Vehicle(v) & Company(c)')

                                                        ],
                                            agent=self,
                                            domain=f'Vehicle({v}) & Route({r}) & Company({self.name})')
                plans.append(new_plan)

        return plans
        

             
            

        

