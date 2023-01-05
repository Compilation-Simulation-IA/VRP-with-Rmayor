import itertools
import numpy as np
import ia.search
from ia.utils import *
from ia.logic import *
from ia.search import *
from ia.planning import *
from agents import Vehicle, Authority, Semaphore, Company
from storage import MapNode


def get_solution(problem):
    solution = uniform_cost_search(ForwardPlan(problem)).solution()
    solution = list(map(lambda action: Expr(action.name, *action.args), solution))
    return solution

def VehicleActions():
    return PlanningProblem(initial='At(V,Deposit) & Adj(Deposit,A) & Adj(A,B) & Adj(B,C) & Adj(C,D) & Adj(D,E) & Adj(E,F) & Adj(F,G) & Empty(Deposit) & Empty(A) & Empty(F) &  Empty(G) & Empty(B) & ~Empty(C) & Empty(D) & ~Empty(E) & FreePass(Deposit) & FreePass(A) & FreePass(F) &  FreePass(G) & ~FreePass(B) & ~FreePass(C) & ~FreePass(D) & FreePass(E) & FreePassA(Deposit) & FreePassA(A) & ~FreePassA(F) &  FreePassA(G) & ~FreePassA(B) & FreePassA(C) & FreePassA(D) & FreePassA(E)',
                            goals='~Empty(G)',
                            actions=[Action('Move(v,x,y)',
                                            precond='Adj(x,y) & At(v,x) & Empty(x) & FreePass(x) & FreePassA(x)',
                                            effect='~At(v,x) & At(v,y)',
                                            domain='Vehicle(v) & Block(x) & Block(y)'),
                                    Action('Load(v,x)',
                                            precond='At(v,x) & ~Empty(x)',
                                            effect='Empty(x)',
                                            domain='Stop(x) & Vehicle(v)'),
                                    Action('Unload(v,x)',
                                            precond = 'At(v,x) & Empty(x)',
                                            effect = '~Empty(x)',
                                            domain= 'Vehicle(v) & End(x)'),
                                    Action('WithAuthority(v,x)',
                                            precond='At(v,x) & Empty(x) & ~FreePassA(x)',
                                            effect= 'FreePassA(x)',
                                            domain='Vehicle(v) & Authority(x)'),
                                    Action('AtSemaphore(v,x)',
                                            precond='At(v,x) & Empty(x) & ~FreePass(x) & FreePassA(x)',
                                            effect= 'FreePass(x)',
                                            domain='Vehicle(v) & Semaphore(x)'),
                                    

                            ],
                            domain='Block(A) & Block(B) & Block(C) & Block(D) & Block(E) & Block(F) & Block(G) & Block(H) & Block(I) & Block(J) & Block(F) &  Block(G) & Block(Deposit) & Vehicle(V)  & Stop(E) & Stop(C) & End(G) & Semaphore(B) & Semaphore(D) & Semaphore(C) & Authority(B) & Authority(F)',
                            )

def CompanyActions():
    return PlanningProblem(initial='~Done(V1,R1) & ~Checked(V1) & ~Payed(V1)',
                            goals='Checked(V1)',
                            actions=[Action('StartRoute(v,r)',
                                            precond='~Done(v,r) & ~Checked(v) & ~Payed(v)',
                                            effect='Done(v,r) & EndRoute(v)',
                                            domain='Vehicle(v) & Route(r)'),
                                    Action('CheckVehicle(v)',
                                            precond='EndRoute(v) & Payed(v) & ~Checked(v)',
                                            effect='Checked(v)',
                                            domain='Vehicle(v)'),
                                    Action('PayTaxes(v)',
                                            precond='~Checked(v) & EndRoute(v) & ~Payed(v)',
                                            effect='Payed(v)',
                                            domain='Vehicle(v)')
                                    
                                    

                            ],
                            domain='Vehicle(V1) & Route(R1)')

n1 = MapNode('(0,0)', 0)
n2 = MapNode('(0,1)', 0)
#n3= MapNode('(0,2)', 0, Authority('(0,2)'), Semaphore("(0,2)"))
#n4 = MapNode('(0,3)', 3)
n5 = MapNode('D', 0, semaphore=Semaphore('D'))
#n6 = MapNode('E', 2)
#n7 = MapNode('F', 0, authority=Authority('F'))
#n8 = MapNode('G', 0)
route = [n1,n2]
vehicle = Vehicle('V',0,0,0.1)
vehicle.route = route
#plan = vehicle.plan()
company = Company('C',200)
#plan = company.plan([('V1','R1')])
#get_solution(plan[0])

li  =[vehicle,'A','B']
dic = Vehicle.__dict__
dic['move'](*li)
#plan =vehicle.plan()
#get_solution(plan)
s = Semaphore((0,0))
node = MapNode((0,0),0,semaphore=s)
s.time_color=15
print(s.color_range)
s.update_color()
print(vehicle.at_semaphore(node))


