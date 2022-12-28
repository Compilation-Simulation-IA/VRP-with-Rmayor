import agents
from storage import *
from agents import *
import random
import math
import networkx as nx


class VRP_Simulation:
    def __init__(self, graph:  Graph, company: Company):
        self.graph_map = graph
        self.company = company
        self.global_time = 0
    
    def sim(self):
        # Simular enrutamiento de vehículos
        while True:
            self.graph_map.update_vehicle_locations()
            self.company.optimize_routes()
            print("Vehicle locations:")
            for vehicle in self.graph_map.vehicles:
                print(f"{vehicle}: {vehicle.current_location}")
            print()
            # Hacer una pausa y volver a iterar
            time.sleep(1)

    def simulate_routing(self):
        while True:
            # Iterar sobre cada uno de los vehículos de la compañía
            for vehicle in self.company.vehicles:
                print("Vehicle locations:")
                print(f"{vehicle}: {vehicle.current_location}")
                print()
                if vehicle.available: #obtiene la ruta asignada al vehículo y el nodo actual en el que se encuentra.
                    actual_route = vehicle.route
                    current_location = vehicle.current_location
                    #Si el nodo actual es un warehouse, significa que el vehículo va a salir del depósito y comenzar su ruta
                    if isinstance(current_location, Warehouse):
                        self.start_route(vehicle, graph, global_time)
                    #Si el nodo actual es una parada de tipo Stop, significa que el vehículo debe recoger a los clientes que se encuentran en esa parada
                    elif isinstance(current_location, Stop):
                        on_board = vehicle.pick_up_clients()
                        self.global_time += 3 * on_board # cada persona se demora 3 min en subir al carro
                        next_node = vehicle.route.next_stop(current_location)
                        vehicle.move(next_node)
                    # Si el nodo actual es un warehouse y el vehículo no está vacío, significa que el vehículo debe dejar a los clientes que lleva abordo en ese depósito
                    elif isinstance(current_location, Warehouse) and vehicle.capacity - vehicle.clients_on_board > 0:
                        off = vehicle.drop_off_clients()
                        self.global_time += 3 * off #tiempo que se demora cada persona en bajar
            self.global_time +=1
            time.sleep(5)
        
    def start_route(self, vehicle: Vehicle, graph: Graph, global_time: float):
        pass

    # Que comience la simulacion del vehiculo id_vehicle en la ruta id_routes
    def start(self, id_vehicle, id_route):
        Actual_State = self.graph_map.currents[id_route]
        Arrival = self.graph_map.target[id_route]
        local_time = 0
        
        while Actual_State != Arrival:
            print(f"Time: {self.global_time}")
            print(Actual_State)
            Actual_State, local_time = self.drive_next_stop(Actual_State, id_vehicle, id_route,local_time)
            self.global_time +=local_time
        print(f"El vehiculo llego al final de la ruta. Parada {Arrival}")

    def drive_next_stop(self,Actual_State, id_vehicle, id_route, local_time):
        """ Moves to the next stop until Arrived at the end """
        next_stop = self.graph_map.routes[id_route].stops[Actual_State.id + 1]
        distance = self.get_distance(Actual_State.coordinates,next_stop.coordinates )
        embark_time = self.get_embark_time(len(next_stop.person_list)) #tiempo mientras se van montando las personas al carro
        local_time += distance + embark_time

        print(f"El vehiculo {id_vehicle} de la ruta {id_route} se movio a la siguiente parada.")
        self.graph_map.currents[id_route] = next_stop
        print(f"El vehiculo {id_vehicle} llego a la parada {next_stop.id}.")

        return next_stop, local_time
    
    #Distancia de Manhattan: start =(x1,y1) , end = (x2,y2)
    def get_distance(self, start, end):
        """Return distance between current and next position in the route"""
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    
    def get_embark_time(self, person_count):
        a = max(3,person_count - 3)
        b = person_count + 3
        return generateUniform(a,b)


# Crear grafo y nodos
graph = Graph()

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

# Crear vehículos y rutas 
vehicle1 = Vehicle(1,"Ford", warehouse1, True, 8, 40000, 10)
vehicle2 = Vehicle(2,"Lada", warehouse1, True, 8, 30000, 10) 

route1 = Route(1, [stop1, stop2, stop3, stop4])
route2 = Route(2, [stop5, stop6, stop7, stop8])

vehicle1.assign_route(route1)
vehicle2.assign_route(route2)

graph.add_node(stop1)
graph.add_node(stop2)
graph.add_node(stop3)
graph.add_node(stop4)
graph.add_node(stop5)
graph.add_node(stop6)
graph.add_node(stop7)
graph.add_node(stop8)

graph.add_node(warehouse1)
graph.add_node(warehouse2)
graph.add_node(warehouse3)

# Inicializar la compañía
company = Company("Compañía de Transporte", 10000)  # Inicializar con un presupuesto de 10000 pesos

# Añadir los warehouses a la compañía
company.add_warehouse(warehouse1)
company.add_warehouse(warehouse2)
company.add_warehouse(warehouse3)

# Añadir los vehículos a la compañía
company.buy_vehicle(vehicle1, 500)
company.buy_vehicle(vehicle2, 300)

# Añadir las rutas a la compañía
company.add_route(route1)
company.add_route(route2)

vrp = VRP_Simulation(graph, company)
vrp.sim()
print("exito")







    