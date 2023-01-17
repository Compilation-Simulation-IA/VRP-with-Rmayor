from storage import MapNode
from agents import Vehicle, Semaphore,Authority, Company
from simulation_logger import Logger
import random
import networkx as nx
import ast
from simulation import VRP_Simulation
import ast


class Generator:

    def __init__(self,vehicles,vehicle_types, clients,stops, depot_company, days, company_budget, map) -> None:
        self.vehicles = vehicles
        self.vehicle_types=vehicle_types
        self.clients=clients
        self.stops = stops
        self.depot_company = depot_company
        self.days= days
        self.company_budget = company_budget
        self.map = map

    def generate_simulation(self):

        """Crea una simulacion"""

        
        stops = self.__process_stops()
        all_stops = {}

        for value in stops.values():
            for stop in value[0]:
                all_stops.update({stop.id:stop})

        map = self.__generate_graph(all_stops)  
        vehicles = self.__process_vehicles(map)
        company = Company('Compañía de Transporte',self.company_budget,map,stops,vehicles,self.depot_company, Logger())
        #poner depot MapNode
        simulation = VRP_Simulation(map,company,self.days)
        
        simulation.start_simulation()



    def __process_stops(self):

        """A partir de lo recibido de la compilacion, 
        se crea un diccionario de la forma 
        { client_id : [[{stop_position:people}],client_depot]}"""

        stops = {}

        for client in self.clients:
            if self.clients[client][2] in  self.stops:
                client_depot = MapNode(self.stops[self.clients[client][2]][0],self.clients[client][2][1])
            client_stops = []
            for s in self.clients[client][1]:
                client_stops.append(MapNode(self.stops[s][0],self.stops[s][1]))
            stops.update({client:[client_stops,client_depot]})

        return stops


    def __process_vehicles(self,map):

        """A partir de lo recibido de la compilacion,
        se crea una lista de vehiculos"""

        
        vehicles =[]
        for vehicle in self.vehicles:
            for i in range(int(self.vehicles[vehicle][1])):
                if self.vehicles[vehicle][0] in self.vehicle_types:
                    name = vehicle
                    capacity = self.vehicle_types[self.vehicles[vehicle][0]][1]
                    miles = self.vehicle_types[self.vehicles[vehicle][0]][2]
                    probability = random.random()
                    logger=Logger()
                    initial=MapNode(self.depot_company,0)
                    vehicle_map=map
                    v = Vehicle(name,capacity,miles,probability,logger,vehicle_map,initial)
                    vehicles.append(v)
        return vehicles

    def __generate_graph(self, all_stops):

        graph = nx.Graph()
        count = 0
        cost = False
        
        with open(self.map,'r') as f:

            while True:
                line = f.readline()
                if not line:
                    break
                semaphore = None
                authority = None
                
                if not line.startswith('Cost') and not cost:
                    line = line[:len(line)-2].removeprefix('[').removesuffix(']')
                    line =line.split(',')                    
                    for i in range(len(line)):
                        index = f'({count},{i})'
                        if int(line[i]) == 1:
                            semaphore = Semaphore(f'({count},{i})')
                        if int(line[i]) == 2:
                            authority = Authority(f'({count},{i})')
                        if int(line[i]) == 3:
                            semaphore = Semaphore(f'({count},{i})')
                            authority = Authority(f'({count},{i})')
                        if index in all_stops.keys():
                            value = all_stops[index]
                            value.authority = authority
                            value.semaphore = semaphore
                            graph.add_node((count,i),value = value)
                        else:
                            graph.add_node((count,i),value = MapNode(f'({count},{i})',0,authority,semaphore))
                elif line.startswith('Cost') or cost:
                    cost = True
                    if line.startswith('Cost'):
                        continue                    
                    line = line.split(':')
                    edge = line[0].split(';') 
                    edge[0]= ast.literal_eval(edge[0].removeprefix('['))
                    edge[1]=ast.literal_eval(edge[1].removesuffix(']'))
                    distance = int(line[1])
                    graph.add_edge(edge[0],edge[1],weight= distance)
        print(graph)
        return graph
                        

gen = Generator([],[],[], [], [], 1, 100, 'map.txt')

                        




         

            

