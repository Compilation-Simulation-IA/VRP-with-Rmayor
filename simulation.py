from storage import *
from agents import *
import random
import math
import networkx as nx
import time
from ia.planning import *
from collections import deque
from ia.utils import *

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
        
    def simulation_vehicle(self,problem, display=False):

        f = memoize(lambda node: node.path_cost, 'f')
        node = Node(problem.initial) # problem.initial is Node state
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()
        response = None
        wait_time = 0

        while frontier:

            if wait_time == 0:
                node = frontier.pop()
                action = problem.actions(node.state)       
                

                if len(action) > 0:
                    action_name = action[0].name
                    print(action_name)
                    action_args = action[0].args
                    print(action_args)
                    response = problem.act(expr(str(action[0])))

                    if action_name == 'move':
                        x = action_args[1]
                        y = action_args[2]
                        edge = graph.get_edge_data(x,y)
                        wait_time += self.cost_move(response, edge['weight'])
                    elif action_name == 'load' or action_name=='unload':
                        wait_time += self.cost_load_and_unload(response)
                    elif action_name == 'at_semaphore':
                        wait_time += response
                    else:
                        pass


                print('action:' + str(action))
                print('Node Frontier: ' + str(node))
                if problem.goal_test(node.state):
                    if display:
                        print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
                    return node
                explored.add(node.state)
                for child in node.expand(problem):
                    print('Frontier Child: ' + str(child))
                    if child.state not in explored and child not in frontier:
                        frontier.append(child)
                    elif child in frontier:
                        if f(child) < frontier[child]:
                            del frontier[child]
                            frontier.append(child)

            else:
                wait_time -=1

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
        
   

    def cost_with_authority(self):
        pass


        

        
graph = nx.Graph()

n1 = MapNode('(0,0)', 0)
n2 = MapNode('(0,1)', 0)
n3= MapNode('(0,2)', 0, Authority('(0,2)'), Semaphore("(0,2)"))
n4 = MapNode('(0,3)', 3)
n5 = MapNode('(0,4)', 0, semaphore=Semaphore('D'))
n6 = MapNode('(0,5)', 2)
n7 = MapNode('(0,6)', 0, authority=Authority('F'))
n8 = MapNode('(0,7)', 0)

graph.add_node((0,0), value=n1)
graph.add_node((0,1), value=n1)
graph.add_node((0,2), value=n3)
graph.add_node((0,3), value=n4)
graph.add_node((0,4), value=n5)
graph.add_node((0,5), value=n6)
graph.add_node((0,6), value=n7)
graph.add_node((0,7), value=n8)


graph.add_edges_from([((0,0),(0,1),{'weight':100}),
                      ((0,1),(0,2),{'weight':120}),
                      ((0,2),(0,3),{'weight':90}),
                      ((0,3),(0,4),{'weight':100}),
                      ((0,4),(0,5),{'weight':110}),
                      ((0,5),(0,6),{'weight':130}),
                      ((0,6),(0,7),{'weight':80}),                      
                       ])

route = [n1,n2,n3,n4,n5,n6,n7,n8]
vehicle = Vehicle('V1', 20, 100, 0.4)
vehicle.route = route
plan = vehicle.plan()

company = Company('C1', 100)
forward_problem = ForwardPlan(plan)
sim = VRP_Simulation(graph,company, 3)
sim.simulation_vehicle(forward_problem)




