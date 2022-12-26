from map_structures import Graph, Node, Edge
from agents import Company,  Client, Authority,  Vehicle
from storage import Route,  Stop, Warehouse
from typing import List
import random
import math
import networkx as nx

def sim1():
        # Inicializar mapa y calles
    map = Map([Street("Main St", 0.5), Street("Maple St", 0.25)], [])

    # Agregar vehículos al mapa
    map.add_vehicle(Vehicle(1, "Main St", "Maple St"))
    map.add_vehicle(Vehicle(2, "Maple St", "Main St"))

    # Simular enrutamiento de vehículos
    while True:
        map.update_vehicle_locations()
        print("Vehicle locations:")
        for vehicle in map.vehicles:
            print(f"Vehicle {vehicle.ID}: {vehicle.current_location}")
        print()
        time.sleep(1)

def sim2():
    # Inicializar empresa
    company = Company([], [], 10000)

    # Agregar almacenes y rutas con sus respectivos vehículos y clientes
    warehouse1 = Warehouse(1, "Location 1", [Vehicle(1, "Model 1", "Location 1", "", True)])
    warehouse2 = Warehouse(2, "Location 2", [Vehicle(2, "Model 2", "Location 2", "", True)])
    route1 = Route(1, ["Customer 1", "Customer 2"], [])
    route2 = Route(2, ["Customer 3", "Customer 4"], [])
    company.add_warehouse(warehouse1)
    company.add_warehouse(warehouse2)
    company.add_route(route1)
    company.add_route(route2)

    # Asignar vehículos a las rutas
    vehicle1 = warehouse1.get_vehicle()
    vehicle2 = warehouse2.get_vehicle()
    route1.assign_vehicle(vehicle1)
    route2.assign_vehicle(vehicle2)

    # Optimizar rutas
    while True:
        company.optimize_routes()
        # Hacer una pausa y volver a iterar
        time.sleep(1)

class VRP_Simulation:
    def __init__(self, graph_map):
        self.graph_map = graph_map
        self.global_time = 0
        #Inicializar los currents de todas las rutas
        for index, r in enumerate(self.graph_map.routes):
            self.graph_map.currents.append(self.graph_map.routes[index].stops[0]) #Departure
            final = len(self.graph_map.routes[index].stops) - 1
            self.graph_map.target.append(self.graph_map.routes[index].stops[final])
        
        
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


    def create_random_map(self, company, client_list, stop_count, person_count_list):
        """Crear mapa aleatorio de la ciudad. Cada nodo es un stop inicializado con sus valores 
        inicializados."""
        graph_map = nx.Graph()
        stop_list = []
        
        graph_map.add_node(company)
        graph_map.add_nodes_from(client_list)

        #En en mapa grafo cada nodo es una parada,compañia o cliente. Todos  tienen una
        # posicion geografica en el mapa. Lo q se tiene es la distancia entre cada uno.
        for i in range (stop_count):
            new_stop = Stop(i, person_count_list[i])
            stop_list.append(new_stop)
            graph_map.add_node(new_stop)
        
        route = Route(0,stop_list) 
        city_map.insert_company(company)
        city_map.insert_route(route)

        #Añadir los costos de las aristas de todos los nodos del grafo
        for i in graph_map:
            for j in graph_map:
                if i!=j:
                    cost = random.randint(1,10)
                    graph_map.add_weighted_edges_from(i,j,cost)
        
        return graph_map



company = Company(0)
client = Client(0)
vehicle = Vehicle(0,"Lada", 4, 10)

company.add_client(client)
company.buy_vehicle(vehicle)
company.assign_vehicle(client, vehicle)
person_count_list = [1,1,1,1,1] # donde el tamaño de la lista es igual a la cantidad de stops

vrp = VRP_Simulation(city_map) #arreglar
vrp.create_random_map(company, [client], 5,person_count_list)
vrp.start(0,0)
print("exito")
    