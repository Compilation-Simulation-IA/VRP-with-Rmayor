from storage import *
from agents import *

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
        self.go_back = False
        self.current_date = 1
        self.days = days
        self.week_day = WeekDays.Lunes.name
        
    def start_simulation(self):
        while self.current_date <= self.days:
            company.logger.log(f"Día {self.week_day} {self.current_date}:")
            plan_company = company.plan()
            simulate_threads = []

            for i,p in enumerate(plan_company):#AQUI VAN LOS HILOS
                forward_problem_company = ForwardPlan(p)
                thread = threading.Thread(target= sim.simulation_Company, args= (forward_problem_company, i) )
                simulate_threads.append(thread)
                print(thread.getName())
                thread.start() # Iniciamos los hilos

            for t in simulate_threads: # Esperamos a que todos los hilos terminen
                t.join()

            # Una vez que todos los hilos han terminado, podemos mostrar el tiempo total transcurrido
            company.logger.log(f"Termino el día.")
            #company.logger.log(f"El tiempo total transcurrido fue de {global_time} segundos")
            self.current_date +=1
            self.week_day = WeekDays(self.current_date % 7).name
            time.sleep(1)
        company.logger.log("FIN")


    def simulation_vehicle(self,problem, global_time):
        f = memoize(lambda node: node.path_cost, 'f')
        node = Node(problem.initial) # problem.initial is Node state
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        response = None
        wait_time = 0
        
        while frontier:
            if wait_time == 0:   
                current_pos = problem.planning_problem.agent.current_location

                if current_pos.authority != None:
                    decision = current_pos.authority.stop_vehicle(problem.planning_problem.agent)
                    if decision == 2:
                        new_route = self.relocate_route(current_pos.id, problem.planning_problem.agent.route)
                        problem.planning_problem.agent.route = new_route
                        problem = ForwardPlan(problem.planning_problem.agent.plan())
                        frontier = PriorityQueue('min', f)
                        frontier.append(Node(problem.initial)) 
                        current_pos.authority = None

                    temp = self.cost_with_authority(decision)
                    wait_time += temp
                    self.company.logger.log(f"{problem.planning_problem.agent} HIZO LA ACCION AUTHORITY: {decision} en el tiempo {global_time}")
                    self.company.logger.log(f" EL COSTO FUE DE {temp}")

                node = frontier.pop()
                action = problem.actions(node.state)
                
                if len(action) > 0:
                    action_name = action[0].name
                    action_args = action[0].args
                    response = problem.act(expr(str(action[0])))
                    self.company.logger.log(f"{problem.planning_problem.agent} HIZO LA ACCION {action[0]} en el tiempo {global_time}")
                    if action_name == 'move':
                        x = action_args[1]
                        y = action_args[2]
                        edge = graph.get_edge_data(x,y)
                        temp = self.cost_move(response, edge['weight'])
                        wait_time += temp
                        self.company.logger.log(f" EL COSTO FUE DE {temp}")
                    elif action_name == 'load' or action_name=='unload':
                        temp = self.cost_load_and_unload(response)
                        wait_time += temp
                        self.company.logger.log(f" EL COSTO FUE DE {temp}")
                    elif action_name == 'at_semaphore':
                        wait_time += response
                        self.company.logger.log(f" EL COSTO FUE DE {response}")
                    else:
                        pass
               
                if problem.goal_test(node.state):
                    self.company.logger.log(f"{problem.planning_problem.agent} termino en {global_time}")
                    
                    return node
                explored.add(node.state)
                for child in node.expand(problem):
                    #print('Frontier Child: ' + str(child))
                    if child.state not in explored and child not in frontier:
                        frontier.append(child)
                    elif child in frontier:
                        if f(child) < frontier[child]:
                            del frontier[child]
                            frontier.append(child)
                #global_time += wait_time  # Actualizamos el tiempo global
            else:
                wait_time -=1
            global_time += 1
            
        return None
    
    def simulation_Company(self, problem, index: int):
        global_time = 0# Declaramos que vamos a usar la variable global

        f = memoize(lambda node: node.path_cost, 'f')
        node = Node(problem.initial) # problem.initial is Node state
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        response = None
        while frontier:
                
            current_vehicle = list(problem.planning_problem.agent.routes.keys())[index]
            current_route = list(problem.planning_problem.agent.routes.values())[index]
            node = frontier.pop()
            action = problem.actions(node.state)       
            
            if len(action) > 0:
                action_name = action[0].name
                response = problem.act(expr(str(action[0])))
                if action_name == 'start_route':
                    forward_problem_vehicle = ForwardPlan(response)
                    self.simulation_vehicle(forward_problem_vehicle, global_time)
                    
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
    




       

    

graph = nx.Graph()

n1 = MapNode('(2,0)', 0)
n2 = MapNode('(2,1)', 0)
n3= MapNode('(2,2)', 0, semaphore= Semaphore('(2,2)'))
n4 = MapNode('(2,3)', 3, authority= Authority('(2,3)', map =graph, probability = 0))
n5 = MapNode('(2,4)', 0)#, semaphore=Semaphore('(2,4)'))
n6 = MapNode('(2,5)', 2)
n7 = MapNode('(2,6)', 0, authority=Authority('(2,6)', map=graph))
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
logger = Logger()

stop_list= [MapNode('(0,0)', 1), MapNode('(1,1)', 1), MapNode('(2,2)', 1), MapNode('(7,7)', 1), MapNode('(6,6)', 1), MapNode('(4,4)', 1), MapNode('(5,5)', 1)]
G, nodes_color = generate_random_graph(stop_list, (3,3))
print(G.edges())
write_map(G, 'map_in')
print("FIN")
#nx.draw(G, node_color= nodes_color)
#plt.show()

#logger = Logger()
#
#route1 = [n1,n2,n3,n4,n5,n6,n7,n8]
#route2 = [n1,n2,n3,n4,n5]
#vehicle1 = Vehicle('V1', 20, 100, 0.0, logger)
#vehicle2 = Vehicle('V2', 10, 100, 1.0, logger)
#vehicle1.route = route1
#vehicle2.route = route2
#
#vehicles = [vehicle1, vehicle2]
#stops = {'client1':[], 'client2':[]}
#company = Company('C1', 100, graph, stops, vehicles, logger)
#company.vehicles.append(vehicle1)
#company.vehicles.append(vehicle2)
#
#company.routes[vehicle1] =  route1
#company.routes[vehicle2] =  route2
#
#company.assignations.append({'V1':vehicle1, 'R1':route1})
#company.assignations.append({'V2':vehicle2, 'R1':route2})
#
#sim = VRP_Simulation(graph,company, 1)
#sim.start_simulation()
#
#print()
#print(company)
#info = company.logger.get_logs()
##info_strings = [str(elem) for elem in info]
#info_result = "\n".join(info)
#print(info_result)
#with open('30_simulations.txt', 'w') as f:
#    f.write(info_result)
#
#print("FIN 2.0")
#
