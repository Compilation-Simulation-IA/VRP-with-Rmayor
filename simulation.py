from storage import *
from agents import *
from generator_random_map import generate_random_graph, write_map

import random
import math
import networkx as nx
import time
from ia.planning import *
from collections import deque
from ia.utils import *
from heapq import heappush, heappop
import ast
import threading
from simulation_logger import Logger
import matplotlib.pyplot as plt

class WeekDays(Enum):
    Lunes = 0
    Martes = 1
    Miércoles = 2
    Jueves = 3
    Viernes = 4
    Sábado = 5
    Domingo = 6

class VRP_Simulation:
    def __init__(self, graph, company: Company, days: int):
        self.graph_map = graph
        self.company = company
        self.map_copy =  graph.copy()
        self.stops_with_people = {}
        self.save_stops()
        self.go_back = False
        self.current_date = 0
        self.days = days
        self.week_day = WeekDays.Lunes.name
        
    def start_simulation(self):
        while self.current_date <= self.days:
            if self.company.bankruptcy():
               self.company.logger.log(f"La Compañia quedo en bancarrota.\n")
               break

            self.company.logger.log(f"Día {self.week_day} {self.current_date + 1}:\n")
            plan_company = self.company.plan()
            simulate_threads = []
            l = threading.Lock()
            for i,p in enumerate(plan_company):#AQUI VAN LOS HILOS
                forward_problem_company = ForwardPlan(p)
                thread = threading.Thread(target= self.simulation_Company, args= (forward_problem_company, i, l) )
                simulate_threads.append(thread)
                thread.start() # Iniciamos los hilos

            for t in simulate_threads: # Esperamos a que todos los hilos terminen
                t.join()

            self.company.logger.log(f"Termino el día.\n") 
            self.company.logger.log(f"Capital de {self.company}: {round(self.company.budget,2)}")
            self.current_date +=1
            self.week_day = WeekDays(self.current_date % 7).name
            self.company.check_maintenance()
            self.load_stops()
            self.change_authorities_places()
            time.sleep(1)

        self.company.logger.log("FIN")
        self.write_logs()

    def save_stops(self):
        for c_i in list(self.company.clients.values()):
            for stop in c_i[0]:
                new_stop = stop.copy()
                self.stops_with_people[new_stop.id] = new_stop.people
    
    def load_stops(self):
        for key in self.stops_with_people.keys():
            self.graph_map.nodes()[eval(key)]['value'].people =  self.stops_with_people[key]
            
    def change_authorities_places(self):
        count_authorities = 0
        for key in self.graph_map.nodes().keys():
            if self.graph_map.nodes()[key]['value'].authority != None:
                count_authorities += 1
                self.graph_map.nodes()[key]['value'].authority = None
        
        lim = list(self.graph_map.nodes())[len(self.graph_map.nodes()) - 1]
        #Puede crear menos semaforos si el random da una posicion invalida
        while count_authorities != 0:
            position = (random.randint(0, lim[0] - 1), random.randint(0, lim[1] - 1))
            if self.graph_map.nodes()[position]['value'].authority == None:
                a = Authority(position, 0.3)
                map_node = self.graph_map.nodes()[position]['value']
                map_node.authority = a
                self.graph_map.nodes()[position].update({'value': map_node})
                count_authorities -= 1

    def write_logs(self):
        info = self.company.logger.get_logs()
        #info_strings = [str(elem) for elem in info]
        info_result = "\n".join(info)
        with open('30_simulations.txt', 'w') as f:
            f.write(info_result)


    def simulation_vehicle(self,vehicle, global_time):
        wait_time = 0
        
        while not vehicle.goal_test():
            if wait_time == 0: 
                current_pos = vehicle.current_location
                action = vehicle.plan()                              
                if action == 'at_authority':
                    decision = current_pos.authority.stop_vehicle(vehicle, self.graph_map, global_time)
                    vehicle.at_authority(decision, global_time)
                    temp = self.cost_with_authority(decision)
                    wait_time += temp
                elif action == 'move':
                    speed, cost = vehicle.move(global_time) 
                    temp = self.cost_move(speed, cost)
                    wait_time += temp
                elif action == 'load' or action=='unload':
                    people = vehicle.load(global_time) if action =='load' else vehicle.unload(global_time)
                    temp = self.cost_load_and_unload(people)
                    wait_time += temp
                elif action == 'at_semaphore':
                    current_pos.semaphore.update_color(global_time)
                    semaphore_time = vehicle.at_semaphore(global_time)
                    wait_time += semaphore_time
                elif action == 'broken':
                    time_broken, cost = vehicle.broken(global_time)
                    self.company.budget -= cost
                    wait_time += time_broken
                    
                #global_time += wait_time  # Actualizamos el tiempo global
            else:
                wait_time -=1
            global_time += 1

        self.company.logger.log(f"{str(datetime.timedelta(seconds = global_time))} {vehicle} terminó ruta con una distancia de {vehicle.distance} km.\n")
            
        return None
    
    def simulation_Company(self, problem, index: int, lock:threading.Lock()):
        global_time = 0# Declaramos que vamos a usar la variable global

        f = memoize(lambda node: node.path_cost, 'f')
        node = Node(problem.initial) # problem.initial is Node state
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        response = None
        with lock:
            while frontier:
                node = frontier.pop()
                action = problem.actions(node.state)       

                if len(action) > 0:
                    action_name = action[0].name
                    response = problem.act(expr(str(action[0])))
                    if action_name == 'start_route':
                        self.simulation_vehicle(response, global_time)

                if problem.goal_test(node.state):
                    #company.logger.log(f"El vehiculo {self.company.vehicles[index]} ha llegado a su destino en {global_time} segundos")
                    return node
                explored.add(node.state)
                for child in node.expand(problem):
                    if child.state not in explored and child not in frontier:
                        frontier.append(child)
                    elif child in frontier:
                        if f(child) < frontier[child]:
                            del frontier[child]
                            frontier.append(child)
        return None

    def cost_move(self, speed, distance): 

        """Calcula el tiempo de recorrer la artista. La velocidad se da en km/h, 
        la distancia en metros y el tiempo resultante se da en segundos"""

        speed = speed * (1000/3600)
        result_time = int(distance / speed)

        return result_time    
      

    def cost_load_and_unload(self, people):

        """Calcula el tiempo de un vehiculo en una parada. El tiempo se da en segundos.
        Utilizamis logaritmo porque mientras mayor cantidad de personas, el tiempo no debe aumentar mucho."""

        return int(math.log(people + 1, 1.6) * 60)        
   

    def cost_with_authority(self, decision: int):
        if decision == 1: #se le puso una multa
            return random.randint(3,10)
        elif decision == 2: #desvia el vehiculo
            return random.randint(3,5)
        return 0

    def heuristic(self,a, b):
        """distancia Manhatan"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    
    
graph = nx.Graph()

n1 = MapNode('(2,0)', 0)
n2 = MapNode('(2,1)', 0)
n3= MapNode('(2,2)', 0, semaphore= Semaphore('(2,2)'))
n4 = MapNode('(2,3)', 3, authority= Authority('(2,3)', probability = 0))
n5 = MapNode('(2,4)', 0)#, semaphore=Semaphore('(2,4)'))
n6 = MapNode('(2,5)', 2)
n7 = MapNode('(2,6)', 0, authority=Authority('(2,6)'))
n8 = MapNode('(2,7)', 0)
n9 = MapNode('(1,3)', 0)
n10 = MapNode('(0,4)', 0)
n11 = MapNode('(1,5)', 0)
n12 = MapNode('(3,4)', 0)
n13 = MapNode('(3,5)', 0)


graph.add_node((2,0), value=n1)
graph.add_node((2,1), value=n2)
graph.add_node((2,2), value=n3)
graph.add_node((2,3), value=n4)
graph.add_node((2,4), value=n5)
graph.add_node((2,5), value=n6)
graph.add_node((2,6), value=n7)
graph.add_node((2,7), value=n8)
graph.add_node((1,3), value=n9)
graph.add_node((0,4), value=n10)
graph.add_node((1,5), value=n11)
graph.add_node((3,4), value=n12)
graph.add_node((3,5), value=n13)



graph.add_edges_from([((2,0),(2,1),{'weight':100}),
                      ((2,1),(2,2),{'weight':120}),
                      ((2,2),(2,3),{'weight':90}),
                      ((2,3),(2,4),{'weight':100}),
                      ((2,4),(2,5),{'weight':110}),
                      ((2,5),(2,6),{'weight':130}),
                      ((2,6),(2,7),{'weight':80}), 
                      ((2,3),(1,3),{'weight':80}),
                      ((0,4),(1,3),{'weight':80}),
                      ((1,5),(0,4),{'weight':80}),
                      ((1,5),(2,5),{'weight':80}),
                      ((2,3),(3,4),{'weight':80}),
                      ((3,5),(3,4),{'weight':80}),
                      ((3,5),(2,5),{'weight':80}),
                                         
                       ])

# stops = {'c1':[[MapNode('(4, 0)',3),MapNode('(2, 3)',2),MapNode('(6, 8)',6)],MapNode('(8, 7)',0)],'c2':[[MapNode('(1, 1)',3),MapNode('(5, 6)',3)],MapNode('(7, 7)',0)],'c3':[[MapNode('(3, 3)',4),MapNode('(2, 1)',3),MapNode('(4, 7)',3)],MapNode('(9, 9)',0)]}
# all_stops = []
# for value in stops.values():
#     for stop in value[0]:
#         all_stops.append(stop)
#     all_stops.append(value[1])
# map = generate_random_graph(all_stops,(10,10))
# # write_map(map, 'map_test')
# logger = Logger()
# vehicles = [Vehicle('V1',5,5,0.5,logger,map,MapNode('(5, 5)',people=0)),Vehicle('V2',5,5,0.5,logger,map,MapNode('(5, 5)',people=0)),Vehicle('V3',10,5,0.5,logger,map,MapNode('(5, 5)',people=0)),Vehicle('V4',8,5,0.5,logger,map,MapNode('(5, 5)',people=0)),Vehicle('V5',8,5,0.5,logger,map,MapNode('(5, 5)',people=0))]
# company = Company('Compañia',10000,map,stops,vehicles,MapNode('(5, 5)',people=0),logger)
# sim = VRP_Simulation(map, company,7)
# sim.start_simulation()