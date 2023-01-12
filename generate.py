from storage import MapNode
from agents import Vehicle, Semaphore,Authority, Company
from simulation_logger import Logger
import random
import networkx as nx
import ast
from simulation import VRP_Simulation


class Generator:

    def __init__(self,vehicles, stops, depot_company, days, company_budget, map) -> None:
        self.vehicles = vehicles
        self.stops = stops
        self.depot_company = depot_company
        self.days= days
        self.company_budget = company_budget
        self.map = map

    def generate_simulation(self):

        """Crea una simulacion"""

        vehicles = self.__process_vehicles()
        stops = self.__process_stops()
        all_stops = []

        for value in stops.values():
            for stop in value:
                all_stops.append(stop)

        map = self.__generate_graph(all_stops)  
        company = Company('Compañía de Transporte',self.company_budget,map,stop,vehicles,self.depot_company, Logger())

        simulation = VRP_Simulation(map,company,self.days)
        
        simulation.start_simulation()



    def __process_stops(self):

        """A partir de lo recibido de la compilacion, 
        se crea un diccionario de la forma 
        { client_id : [[{stop_position:people}],client_depot]}"""

        stops = {}

        for stop in self.stops.values():
            client_id = stop[0]
            client_depot = {stop[2].address:stop[2].people}
            client_stops = []
            for s in stop[1]:
                client_stops.append({s.address:s.people})
            stops.update({client_id:[client_stops,client_depot]})

        return stops


    def __process_vehicles(self):

        """A partir de lo recibido de la compilacion,
        se crea una lista de vehiculos"""

        
        vehicles =[]

        for vehicle in self.vehicles.values():
            for i in range(int(vehicle[1])):
                name = str(vehicle[0][0].name) + str(i)
                capacity = vehicle[0][0].capacity
                miles = vehicle[0][0].miles
                probability = random.random()
                v = Vehicle(name,capacity,miles,probability)
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
                obstacle = False
                people = 0
                if not line.startswith('Cost') and not cost:
                    line = line.removeprefix('[').removesuffix(']')
                    line =line.split(',')                    
                    for i in range(len(line)):
                        if int(line[i]) == 1:
                            semaphore = Semaphore(f'({count},{i})')
                        if int(line[i]) == 2:
                            authority = Authority(f'({count},{i})')
                        if int(line[i]) == 3:
                            semaphore = Semaphore(f'({count},{i})')
                            authority = Authority(f'({count},{i})')
                        if (count, i) in all_stops.keys():
                            people = all_stops[(count, i)]
                        graph.add_node((count,i),value = MapNode(f'({count},{i})',people,authority,semaphore))
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
                        

gen = Generator([], [], [], 1, 100, 'map.txt')

                        




         

            

