import agents
from storage import *
from agents import *
import random
import math
import networkx as nx

class VRP_Simulation:
    def __init__(self, graph, company: Company):
        self.graph_map = graph
        self.company = company
        self.global_time = 0
        
    def simulate_routing(self):
        while True:
            print(f"Tiempo: {self.global_time} min")
            # Iterar sobre cada uno de los vehículos de la compañía
            for vehicle in self.company.vehicles:
                if vehicle.available: #obtiene la ruta asignada al vehículo y el nodo actual en el que se encuentra.
                    actual_route = vehicle.route
                    current_location = vehicle.current_location
                    self.print_vehicle_locations(vehicle)
                    #El tiempo pasa mientras el vehiculo hace otra funcion
                    if vehicle.wait > 0:
                        if vehicle.wait - 1 == 0:#ultimo ciclo de espera
                            if vehicle.state == 1:
                                next_node = vehicle.route.next_stop(current_location)
                                cost = self.graph_map.get_edge_data(current_location, next_node)['weight']
                                vehicle.move(next_node, cost)
                                vehicle.actual_stop_index = actual_route.stops.index(next_node)
                            vehicle.total_time_wait = 0
                        vehicle.wait -= 1
                    # Si el nodo actual es un warehouse, significa que el vehículo va a salir del depósito y comenzar su ruta
                    # El vehiculo termino de recoger a los clientes de esa parada y se dispone a ir a la siguiente parada
                    # El vehiculo llega a una parada donde no tiene q recoger a nadie entonces continua (isinstance(current_location, None))
                    elif (isinstance(current_location, Warehouse) and vehicle.state == 0) or (isinstance(current_location, Stop) and vehicle.state == 2) or ((not isinstance(current_location, Stop) and not isinstance(current_location, Warehouse)) and vehicle.state == 1):
                        next_node = vehicle.route.next_stop(current_location)
                        edge = self.graph_map.get_edge_data(current_location, next_node)
                        vehicle.wait = vehicle.total_time_wait = edge['weight']
                        vehicle.state = 1
                    #Si el nodo actual es una parada de tipo Stop, significa que el vehículo debe recoger a los clientes que se encuentran en esa parada
                    elif isinstance(current_location, Stop) and vehicle.state == 1:
                        on_board = vehicle.pick_up_clients()
                        vehicle.wait = vehicle.total_time_wait = on_board # cada persona se demora 3 min en subir al carro
                        vehicle.state = 2
                    # Si el nodo actual es el ultimo de la ruta entonces se bajan los clientes
                    elif actual_route.actual_stop_index == len(actual_route) - 1 and vehicle.state == 1:
                        off = vehicle.drop_off_clients()
                        vehicle.wait = vehicle.total_time_wait = off #tiempo que se demora cada persona en bajar
                        vehicle.state = 3
                    # El vehiculo termino la ruta => comprobar su estado para mandarlo a mantenimiento
                    elif vehicle.state == 3:
                        vehicle.miles
                        company.check_vehicle(vehicle)
                        vehicle.state = 4
                        vehicle.wait = vehicle.total_time_wait = 10 # espera 10 unidades de tiempo
                        vehicle.total_time_wait = 0
                else:
                    #El vehiculo esta en mantenimiento y en un warehouse
                    if vehicle.wait - 1 == 0 and vehicle.state == 4:
                        vehicle.available = True
                        company.check_vehicle(vehicle)
                        vehicle.total_time_wait = vehicle.state = 0
                    vehicle.wait -= 1

            self.global_time +=1
            time.sleep(5)
        
    
    def print_vehicle_locations(self, vehicle: Vehicle):
        print("Vehicle locations:")
        if vehicle.wait == 0 :
            print(f"{vehicle}: Location {vehicle.current_location}")
        else:
            percent_value = (1 - vehicle.wait/vehicle.total_time_wait)* 100
            if vehicle.state == 1: 
                next_node = vehicle.route.next_stop(current_location)
                print(f"El vehículo {vehicle} se está moviendo de {vehicle.current_location} a {next_node}({percent_value}%).")
            elif vehicle.state == 2:
                print(f"El vehículo {vehicle} está cargando pasajeros en {vehicle.current_location}({percent_value}%).")
            elif vehicle.state == 3:
                print(f"El vehículo {vehicle} está descargando pasajeros en {vehicle.current_location}({percent_value}%).")
            elif vehicle.state == 4:
                print(f"El vehículo {vehicle} está en manteniemiento en {vehicle.current_location}({percent_value}%).")
        print()
        

    # Que comience la simulacion del vehiculo id_vehicle en la ruta id_routes
    #def start(self, id_vehicle, id_route):
    #    Actual_State = self.graph_map.currents[id_route]
    #    Arrival = self.graph_map.target[id_route]
    #    local_time = 0
    #    
    #    while Actual_State != Arrival:
    #        print(f"Time: {self.global_time}")
    #        print(Actual_State)
    #        Actual_State, local_time = self.drive_next_stop(Actual_State, id_vehicle, id_route,local_time)
    #        self.global_time +=local_time
    #    print(f"El vehiculo llego al final de la ruta. Parada {Arrival}")
#
    #def drive_next_stop(self,Actual_State, id_vehicle, id_route, local_time):
    #    """ Moves to the next stop until Arrived at the end """
    #    next_stop = self.graph_map.routes[id_route].stops[Actual_State.id + 1]
    #    distance = self.get_distance(Actual_State.coordinates,next_stop.coordinates )
    #    embark_time = self.get_embark_time(len(next_stop.person_list)) #tiempo mientras se van montando las personas al carro
    #    local_time += distance + embark_time
#
    #    print(f"El vehiculo {id_vehicle} de la ruta {id_route} se movio a la siguiente parada.")
    #    self.graph_map.currents[id_route] = next_stop
    #    print(f"El vehiculo {id_vehicle} llego a la parada {next_stop.id}.")
#
    #    return next_stop, local_time
    
    #Distancia de Manhattan: start =(x1,y1) , end = (x2,y2)
    def get_distance(self, start, end):
        """Return distance between current and next position in the route"""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    def get_embark_time(self, person_count):
        a = max(3,person_count - 3)
        b = person_count + 3
        return generateUniform(a,b)


# Crear grafo y nodos
graph = nx.Graph()

# Crear paradas
stop1 = Stop(1, 2, (0, 0), 3)
stop2 = Stop(2, 2, (1, 1), 3)
stop3 = Stop(3, 1, (2, 2), 3)
stop4 = Stop(4, 0, (3, 3), 3)
stop5 = Stop(5, 1, (4, 4), 3)
stop6 = Stop(6, 2, (5, 5), 3)
stop7 = Stop(7, 1, (6, 6), 3)
stop8 = Stop(8, 2, (7, 7), 3)

warehouse1 = Warehouse(9 , (8, 8))
warehouse2 = Warehouse(10, (9, 9))
warehouse3 = Warehouse(11, (10, 10))

# Crea una lista de tuplas con los nodos y sus atributos
nodos = [stop1,stop2,stop3,stop4,stop5,stop6,stop7,stop8,warehouse1,warehouse2,warehouse3]

# Añadir nodos
graph.add_nodes_from(nodos)

# Crea una lista de tuplas con las aristas y sus atributos
aristas = [
    (nodos[8], nodos[0], 1),
    (nodos[0], nodos[1], 1),
    (nodos[1], nodos[2], 1),
    (nodos[2], nodos[3], 1),
    (nodos[3], nodos[9], 1),
    (nodos[8], nodos[4], 2),
    (nodos[4], nodos[5], 2),
    (nodos[5], nodos[6], 2),
    (nodos[6], nodos[7], 2),
    (nodos[7], nodos[10], 2),
]

# Añadir aristas
graph.add_weighted_edges_from(aristas)
print(list(graph.nodes)[0])

# Crear vehículos y rutas 
vehicle1 = Vehicle(1,"Ford", nodos[8], True, 8, 0, 50, 5)
vehicle2 = Vehicle(2,"Lada", nodos[8], True, 8, 0, 30, 5) 

r1 = [nodos[8], nodos[0], nodos[1], nodos[2], nodos[3], nodos[9]]
r2 = [nodos[8], nodos[4], nodos[4], nodos[6], nodos[7], nodos[10]]
route1 = Route(1, r1)
route2 = Route(2, r2)

vehicle1.assign_route(route1)
vehicle2.assign_route(route2)

# Inicializar la compañía
company = Company("Compañía de Transporte", 10000)  # Inicializar con un presupuesto de 10000 pesos

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

vrp = VRP_Simulation(graph, company)
vrp.simulate_routing()
print("exito")







    