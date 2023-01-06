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
                    wait_time += self.cost_with_authority(decision)

                        

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
#n2 = MapNode('(2,1)', 0)
#n3= MapNode('(2,2)', 0, semaphore= Semaphore('(2,2)'))
n4 = MapNode('(2,3)', 3, authority= Authority('(2,3)', map =graph, probability = 1))
n5 = MapNode('(2,4)', 0, semaphore=Semaphore('(2,4)'))
n6 = MapNode('(2,5)', 2)
n7 = MapNode('(2,6)', 0, authority=Authority('(2,6)', map=graph))
n8 = MapNode('(2,7)', 0)
n9 = MapNode('(1,3)', 0)
n10 = MapNode('(0,4)', 0)
n11 = MapNode('(1,5)', 0)
n12 = MapNode('(3,4)', 0)
n13 = MapNode('(3,5)', 0)


graph.add_node((2,0), value=n1)
#graph.add_node((2,1), value=n2)
#graph.add_node((2,2), value=n3)
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



graph.add_edges_from([((2,0),(2,3),{'weight':100}),
                      #((2,1),(2,2),{'weight':120}),
                      #((2,2),(2,3),{'weight':90}),
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

route = [n1,n4,n5,n6,n7,n8]
vehicle = Vehicle('V1', 20, 100, 0.4)
vehicle.route = route
plan = vehicle.plan()

company = Company('C1', 100,graph)
forward_problem = ForwardPlan(plan)
sim = VRP_Simulation(graph,company, 3)
sim.simulation_vehicle(forward_problem)
#path = sim.relocate_route('(2,3)',route)
#for p in path:
#    print(p.id)
#node = nx.get_node_attributes(graph,'value')

#print(nx.shortest_path(graph,(2,3),(2,5), weight='weight'))
#print(list(graph.neighbors((2,3))))
#print(graph[(2,3)][(2,4)]['weight'])

print(ast.literal_eval(route[0].id) == (2,0))