import agents
from storage import *
from agents import *
import random
import math
import networkx as nx
import time

class WeekDays(Enum):
    Lunes = 1
    Martes = 2
    Miércoles = 3
    Jueves = 4
    Viernes = 5
    Sábado = 6
    Domingo = 7

class VRP_Simulation:
    def __init__(self, graph, company: Company, days: int):
        self.graph_map = graph
        self.company = company
        self.global_time = 0
        self.go_back = False
        self.current_date = 1
        self.days = days
        self.week_day = WeekDays.Lunes.name
        
    #def simulate_routing(self):
    #    print("Comienza la simulación")
    #    while self.current_date <= self.days:
    #        print(f"Día {self.current_date}, {self.week_day}")
    #        print()
    #        self.global_time = 0
    #        while True:
    #            end = 0
    #            print(f"Tiempo: {self.global_time} min")
    #            # Iterar sobre cada uno de los vehículos de la compañía
    #            for vehicle in self.company.vehicles:
    #                if vehicle.days_off == 0: #obtiene la ruta asignada al vehículo y el nodo actual en el que se encuentra.
    #                    actual_route = vehicle.route
    #                    current_location = vehicle.current_location
    #                    self.print_vehicle_locations(vehicle)
    #                    next_node = vehicle.route.next_stop(current_location)
    #                    edge = self.graph_map.get_edge_data(current_location, next_node)
#
    #                    #El tiempo pasa mientras el vehiculo hace otra funcion
    #                    if vehicle.wait > 0:
    #                        #en la arista donde se esta moviendo el vehiculo hay una autoridad o semaforo:
    #                        if vehicle.state == 1:
    #                            if vehicle.pos_traffic_edge >= 0 and len(edge['weight']['traffic_authorities']) > vehicle.pos_traffic_edge:
    #                                traffic_a = edge['weight']['traffic_authorities'][vehicle.pos_traffic_edge]
    #                                if isinstance(traffic_a, Authority):
    #                                    decision = traffic_a.stop_vehicle(vehicle)
    #                                    if decision in [1,2]:
    #                                        if decision == 2:
    #                                            print(f"El {vehicle} fue parado por la {traffic_a}.")
    #                                            self.recalculate_route()
    #                                        else:
    #                                            print(f"El {vehicle} fue detenido por exceso de velocidad por {traffic_a}.") #entre 10 y 15 min
    #                                        vehicle.wait = vehicle.pos_traffic_edge + 2 #simula el tiempo q se demoro el vehiculo en encontrarse con la autoridad en la arista. Es el tiempo volviendo para atras
    #                                        vehicle.state = 6
    #                                    else:
    #                                        print(f"El {vehicle} paso la {traffic_a} y no lo pararon.")
    #                                else: # isinstance(i, Semaphore)
    #                                    color, semaphore_time = traffic_a.get_color(self.global_time)
    #                                    if color == Color.YELLOW:
    #                                        if vehicle.pass_red():#no hace nada
    #                                            print(f"El {vehicle} NO paró en la luz amarilla del {traffic_a}.")
    #                                            vehicle.pos_traffic_edge += 1
    #                                        else:
    #                                            new_wait = semaphore_time + traffic_a.color_range[2]
    #                                            vehicle.wait += new_wait
    #                                            print(f"El {vehicle} le cogio la luz amarilla en el {traffic_a} y paró. Tiempo de espera: {new_wait}.")
    #                                            vehicle.state = 5
#
    #                                    elif color == Color.RED:
    #                                        vehicle.wait += semaphore_time
    #                                        print(f"El {vehicle} le cogio la luz roja en el {traffic_a}. Tiempo de espera: {semaphore_time}.")
    #                                        vehicle.state = 5  
#
    #                        elif vehicle.state == 5:
    #                            traffic_a = edge['weight']['traffic_authorities'][vehicle.pos_traffic_edge]
    #                            color, semaphore_time = traffic_a.get_color(self.global_time)
    #                            if color == Color.GREEN:
    #                                vehicle.state = 1
    #                                vehicle.pos_traffic_edge += 1
    #                        if vehicle.wait - 1 == 0:#ultimo ciclo de espera
    #                            if vehicle.state == 1:
    #                                next_node = vehicle.route.next_stop(current_location)
    #                                cost = self.graph_map.get_edge_data(current_location, next_node)['weight']
    #                                vehicle.move(next_node, cost)
    #                                actual_route.actual_stop_index = actual_route.stops.index(next_node)
    #                                vehicle.pos_traffic_edge = 0
    #                            elif vehicle.state == 5:
    #                                vehicle.state = 1
    #                                vehicle.pos_traffic_edge += 1
    #                            elif vehicle.state == 6:
    #                                print(f"Recalculando ruta...")
    #                                vehicle.state = 1
    #                                vehicle.pos_traffic_edge += 1
    #                            vehicle.total_time_wait = 0
    #                        vehicle.wait -= 1
    #                    # Si el nodo actual es un warehouse, significa que el vehículo va a salir del depósito y comenzar su ruta
    #                    # El vehiculo termino de recoger a los clientes de esa parada y se dispone a ir a la siguiente parada
    #                    #  El vehiculo esta volviendo y termino de dejar a los clientes de esa parada y se dispone a ir a la siguiente parada
    #                    # El vehiculo llega a una parada donde no tiene q recoger a nadie entonces continua (isinstance(current_location, None))
    #                    elif (isinstance(current_location, Warehouse) and vehicle.state == 0) or (isinstance(current_location, Stop) and (vehicle.state == 2 or vehicle.state == 3)) or ((isinstance(current_location, Stop) and current_location.total_client == 0) and vehicle.state == 1):
    #                        next_node = vehicle.route.next_stop(current_location)
    #                        edge = self.graph_map.get_edge_data(current_location, next_node)
    #                        vehicle.wait = vehicle.total_time_wait = edge['weight']
    #                        vehicle.state = 1
    #                    elif current_location.authority != None:
    #                        pass
    #                    
#
    #                    elif current_location.semaphore != None:
    #                        pass
#
#
#
    #                    #Si el nodo actual es una parada de tipo Stop, significa que el vehículo debe recoger a los clientes que se encuentran en esa parada
    #                    elif isinstance(current_location, Stop) and vehicle.state == 1:
    #                        if self.go_back:
    #                            off = vehicle.drop_off_clients()
    #                            vehicle.wait = vehicle.total_time_wait = off #tiempo que se demora cada persona en bajar
    #                            vehicle.state = 3
    #                        else:
    #                            on_board = vehicle.pick_up_clients()
    #                            vehicle.wait = vehicle.total_time_wait = on_board # cada persona se demora 3 min en subir al carro
    #                            vehicle.state = 2
    #                    # Si el nodo actual es el ultimo de la ruta entonces se bajan los clientes
    #                    # O si esta volviendo el vehiculo, va dejando a los clientes en sus respectivas paradas
    #                    elif actual_route.actual_stop_index == len(actual_route.stops) - 1 and vehicle.state == 1 and not self.go_back:  
    #                        off = vehicle.drop_off_clients()
    #                        vehicle.wait = vehicle.total_time_wait = off #tiempo que se demora cada persona en bajar
    #                        vehicle.state = 3
    #                    # El vehiculo termino la ruta => comprobar su estado para mandarlo a mantenimiento
    #                    elif end != len(self.company.vehicles) and ((vehicle.state == 3 and not self.go_back) or (vehicle.state == 1 and self.go_back) ):
    #                        company.check_vehicle(vehicle)
    #                        end += 1
#
    #                else:
    #                    #El vehiculo esta en mantenimiento y en un warehouse
    #                    if vehicle.wait - 1 == 0 and vehicle.state == 4:
    #                        vehicle.days_off = 0
    #                        company.check_vehicle(vehicle)
    #                        vehicle.total_time_wait = vehicle.state = 0
    #                    vehicle.wait -= 1
#
    #            if end == len(self.company.vehicles):
    #                print(f"Todos los vehículos concluyeron sus respectivas rutas.")
    #                if not self.go_back:
    #                    print(f"Pasando el tiempo...")
    #                    time.sleep(5)
    #                    self.reorder_rutes()
    #                    self.go_back = True
    #                    taxes = self.company.pay_taxes()
    #                    end = 0
    #                    print(f"{self.company} pagó {taxes} pesos en multas.")
    #            self.global_time +=1
    #            time.sleep(1)
    #            if self.go_back and end == len(self.company.vehicles): #Termino la ruta de vuelta
    #                print(f"Terminaron los recorridos del Día {self.current_date}, {self.week_day}")
    #                break
    #        self.current_date +=1
    #        self.week_day = WeekDays(self.current_date % 7).name
    #        time.sleep(1)
        
    #vuelve al nodo anterior(siempre estuvo alli), recalcula la ruta(cambiar los costos de las aristas),
    # se la pasa al vehiculo, y lo pone en state = 1 en el proximo cambio de tiempo
    def recalculate_route(self):
        pass
    
    def generate_vehicle(self):
        vehicle3 = Vehicle(3,"Lada", nodos[8], 8, 0, 30, 5, 0.8)
        pass
    def reorder_rutes(self):
        """Este metodo ordena todas las rutas de atras para alante. La ultima parada sera la 1ra ahora,
         la penultima sera la 2da y asi..."""
        for vehicle in self.company.vehicles:
            vehicle.state = 0
            vehicle.route.stops.reverse()
            # Por cada vehiculo en mantenimiento se busca un sustituto
            if vehicle.days_off > 0:# pq esta en mantenimiento
                for v in self.company.vehicles:
                    if v.days_off == 0 and v.route == []:
                        v.assign_route(vehicle.route)
                        vehicle.unassign_route()
                        break
                # No se pudo asignar la ruta a algun vehiculo.
                if vehicle.route != []: 
                    new_vehicle = self.generate_vehicle()
                    self.company.buy_vehicle(new_vehicle, 100)
            on_board = 0
            for stop in vehicle.route.stops:
                if isinstance(stop, Stop):
                    on_board += stop.total_client
            vehicle.clients_on_board = on_board
    def time_per_block(self, speed: int, weight: int) -> int:
        """Calcula el tiempo que se demora entre los nodos"""

    def print_vehicle_locations(self, vehicle: Vehicle):
        print("Vehicle Location:")
        if vehicle.wait == 0 :
            print(f"{vehicle}: Location {vehicle.current_location}")
        else:
            percent_value = (1 - vehicle.wait/vehicle.total_time_wait)* 100
            if vehicle.state == 1: 
                next_node = vehicle.route.next_stop(vehicle.current_location)
                print(f"El {vehicle} se está moviendo de {vehicle.current_location} a {next_node} ({percent_value}%).")
            elif vehicle.state == 2:
                print(f"El {vehicle} está cargando pasajeros en {vehicle.current_location} ({percent_value}%).")
            elif vehicle.state == 3:
                print(f"El {vehicle} está descargando pasajeros en {vehicle.current_location} ({percent_value}%).")
            elif vehicle.state == 4:
                print(f"El {vehicle} está en manteniemiento en {vehicle.current_location} ({percent_value}%).")
            elif vehicle.state == 5 or vehicle.state == 6:
                next_node = vehicle.route.next_stop(vehicle.current_location)
                edge = self.graph_map.get_edge_data(vehicle.current_location, next_node)
                traffic_a = edge['weight']['traffic_authorities'][vehicle.pos_traffic_edge - 1]
                if vehicle.state == 5:
                    print(f"El {vehicle} está parado en un {traffic_a}.")
                else:
                    print(f"El {vehicle} está volviendo para la parada anterior debido a {traffic_a} ({percent_value}%).")
        print()
    
    #Distancia de Manhattan: start =(x1,y1) , end = (x2,y2)
    def get_distance(self, start, end):
        """Return distance between current and next position in the route"""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])


# Crear grafo y nodos
graph = nx.Graph()


# Crear paradas
stop1 = MapNode(1, Stop(1, 2, (0, 0), 3))
stop2 = MapNode(2, Stop(2, 2, (1, 1), 3))
stop3 = MapNode(3, Stop(3, 1, (2, 2), 3))
stop4 = MapNode(4, Stop(4, 0, (3, 3), 3))
stop5 = MapNode(5, Stop(5, 1, (4, 4), 3))
stop6 = MapNode(6, Stop(6, 2, (5, 5), 3))
stop7 = MapNode(7, Stop(7, 1, (6, 6), 3))
stop8 = MapNode(8, Stop(8, 2, (7, 7), 3))
none1 = MapNode(9, Stop(12, 0, (7, 7), 3)) #Los nodos que no tengan clientes para recoger se consideran paradas vacias
none2 = MapNode(10, Stop(13, 0, (7, 7), 3))

# Setear los valores de las autoridades y los semaforos en los nodos
stop6.authority = Authority(1, 0.5)
stop7.semaphore = Semaphore(1, [3, 1, 2])

warehouse1 = MapNode(Warehouse(9 , (8, 8)))
warehouse2 = MapNode(Warehouse(10, (9, 9)))
warehouse3 = MapNode(Warehouse(11, (10, 10)))

# Crea una lista de tuplas con los nodos y sus atributos
nodos = [stop1, stop2, stop3, stop4, stop5, stop6, stop7, stop8, warehouse1, warehouse2, warehouse3, none1, none2]

# Añadir nodos
graph.add_nodes_from(nodos)

# Crea una lista de tuplas con las aristas y sus atributos
aristas = [
    (nodos[8],  nodos[0] , 1), 
    (nodos[0],  nodos[1] , 1), 
    (nodos[1],  nodos[2] , 1), 
    (nodos[2],  nodos[3] , 1), 
    (nodos[3],  nodos[11], 1),
    (nodos[11], nodos[9] , 1),
    (nodos[8],  nodos[4] , 2), 
    (nodos[4],  nodos[5] , 2),
    (nodos[5],  nodos[6] , 2),
    (nodos[6],  nodos[12], 2),
    (nodos[12], nodos[7] , 2),
    (nodos[7],  nodos[10], 2)
]

# Añadir aristas
graph.add_weighted_edges_from(aristas)
print(graph.nodes())

# Crear vehículos y rutas 
vehicle1 = Vehicle(1,"Ford", nodos[8], 8, 0, 50, 5, 0.5)
vehicle2 = Vehicle(2,"Lada", nodos[8], 8, 0, 30, 5, 0.8) 

r1 = [nodos[8], nodos[0], nodos[1], nodos[2], nodos[3], nodos[9]]
r2 = [nodos[8], nodos[4], nodos[5], nodos[6], nodos[7], nodos[10]]
route1 = Route(1, r1)
route2 = Route(2, r2)

vehicle1.assign_route(route1)
vehicle2.assign_route(route2)

# Inicializar la compañía
company = Company("Compañía de Transporte", 100000)  # Inicializar con un presupuesto de 10000 pesos

# Añadir los warehouses a la compañía
company.add_warehouse(nodos[8])
company.add_warehouse(nodos[9])
company.add_warehouse(nodos[10])

# Añadir los vehículos a la compañía
company.buy_vehicle(vehicle1, 400)
company.buy_vehicle(vehicle2, 300)

# Añadir las rutas a la compañía
company.add_route(route1)
company.add_route(route2)

vrp = VRP_Simulation(graph, company, 3)
vrp.simulate_routing()
print("exito")







    