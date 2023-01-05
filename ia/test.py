import itertools
import numpy as np
import search
from utils import *
from logic import *
from search import *
from planning import *
import random
import math

class PlanningProblem:
    """
    Planning Domain Definition Language (PlanningProblem) used to define a search problem.
    It stores states in a knowledge base consisting of first order logic statements.
    The conjunction of these logical statements completely defines a state.
    """

    def __init__(self, initial, goals, actions, domain=None):
        self.initial = self.convert(initial) if domain is None else self.convert(initial) + self.convert(domain)
        self.goals = self.convert(goals)
        self.actions = actions
        self.domain = domain

    def convert(self, clauses):
        """Converts strings into exprs"""
        if not isinstance(clauses, Expr):
            if len(clauses) > 0:
                clauses = expr(clauses)
            else:
                clauses = []
        try:
            clauses = conjuncts(clauses)
        except AttributeError:
            pass

        new_clauses = []
        for clause in clauses:
            if clause.op == '~':
                new_clauses.append(expr('Not' + str(clause.args[0])))
            else:
                new_clauses.append(clause)
        return new_clauses

    def expand_fluents(self, name=None):

        kb = None
        if self.domain:
            kb = FolKB(self.convert(self.domain))
            for action in self.actions:
                if action.precond:
                    for fests in set(action.precond).union(action.effect).difference(self.convert(action.domain)):
                        if fests.op[:3] != 'Not':
                            kb.tell(expr(str(action.domain) + ' ==> ' + str(fests)))

        objects = set(arg for clause in set(self.initial + self.goals) for arg in clause.args)
        fluent_list = []
        if name is not None:
            for fluent in self.initial + self.goals:
                if str(fluent) == name:
                    fluent_list.append(fluent)
                    break
        else:
            fluent_list = list(map(lambda fluent: Expr(fluent[0], *fluent[1]),
                                   {fluent.op: fluent.args for fluent in self.initial + self.goals +
                                    [clause for action in self.actions for clause in action.effect if
                                     clause.op[:3] != 'Not']}.items()))

        expansions = []
        for fluent in fluent_list:
            for permutation in itertools.permutations(objects, len(fluent.args)):
                new_fluent = Expr(fluent.op, *permutation)
                if (self.domain and kb.ask(new_fluent) is not False) or not self.domain:
                    expansions.append(new_fluent)

        return expansions

    def expand_actions(self, name=None):
        """Generate all possible actions with variable bindings for precondition selection heuristic"""

        has_domains = all(action.domain for action in self.actions if action.precond)
        kb = None
        if has_domains:
            kb = FolKB(self.initial)
            for action in self.actions:
                if action.precond:
                    kb.tell(expr(str(action.domain) + ' ==> ' + str(action)))

        objects = set(arg for clause in self.initial for arg in clause.args)
        expansions = []
        action_list = []
        if name is not None:
            for action in self.actions:
                if str(action.name) == name:
                    action_list.append(action)
                    break
        else:
            action_list = self.actions

        for action in action_list:
            for permutation in itertools.permutations(objects, len(action.args)):
                bindings = unify_mm(Expr(action.name, *action.args), Expr(action.name, *permutation))
                if bindings is not None:
                    new_args = []
                    for arg in action.args:
                        if arg in bindings:
                            new_args.append(bindings[arg])
                        else:
                            new_args.append(arg)
                    new_expr = Expr(str(action.name), *new_args)
                    if (has_domains and kb.ask(new_expr) is not False) or (
                            has_domains and not action.precond) or not has_domains:
                        new_preconds = []
                        for precond in action.precond:
                            new_precond_args = []
                            for arg in precond.args:
                                if arg in bindings:
                                    new_precond_args.append(bindings[arg])
                                else:
                                    new_precond_args.append(arg)
                            new_precond = Expr(str(precond.op), *new_precond_args)
                            new_preconds.append(new_precond)
                        new_effects = []
                        for effect in action.effect:
                            new_effect_args = []
                            for arg in effect.args:
                                if arg in bindings:
                                    new_effect_args.append(bindings[arg])
                                else:
                                    new_effect_args.append(arg)
                            new_effect = Expr(str(effect.op), *new_effect_args)
                            new_effects.append(new_effect)
                        expansions.append(Action(new_expr, new_preconds, new_effects))

        return expansions

    def is_strips(self):
        """
        Returns True if the problem does not contain negative literals in preconditions and goals
        """
        return (all(clause.op[:3] != 'Not' for clause in self.goals) and
                all(clause.op[:3] != 'Not' for action in self.actions for clause in action.precond))

    def goal_test(self):
        """Checks if the goals have been reached"""
        return all(goal in self.initial for goal in self.goals)

    def act(self, action):
        """
        Performs the action given as argument.
        Note that action is an Expr like expr('Remove(Glass, Table)') or expr('Eat(Sandwich)')
        """
        action_name = action.op
        args = action.args
        list_action = first(a for a in self.actions if a.name == action_name)
        if list_action is None:
            raise Exception("Action '{}' not found".format(action_name))
        if not list_action.check_precond(self.initial, args):
            raise Exception("Action '{}' pre-conditions not satisfied".format(action))
        self.initial = list_action(self.initial, args).clauses


class Action:
    """
    Defines an action schema using preconditions and effects.
    Use this to describe actions in PlanningProblem.
    action is an Expr where variables are given as arguments(args).
    Precondition and effect are both lists with positive and negative literals.
    Negative preconditions and effects are defined by adding a 'Not' before the name of the clause
    Example:
    precond = [expr("Human(person)"), expr("Hungry(Person)"), expr("NotEaten(food)")]
    effect = [expr("Eaten(food)"), expr("Hungry(person)")]
    eat = Action(expr("Eat(person, food)"), precond, effect)
    """

    def __init__(self, action, precond, effect, domain=None):
        if isinstance(action, str):
            action = expr(action)
        self.name = action.op
        self.args = action.args
        self.precond = self.convert(precond) if domain is None else self.convert(precond) + self.convert(domain)
        self.effect = self.convert(effect)
        self.domain = domain

    def __call__(self, kb, args):
        return self.act(kb, args)

    def __repr__(self):
        return '{}'.format(Expr(self.name, *self.args))

    def convert(self, clauses):
        """Converts strings into Exprs"""
        if isinstance(clauses, Expr):
            clauses = conjuncts(clauses)
            for i in range(len(clauses)):
                if clauses[i].op == '~':
                    clauses[i] = expr('Not' + str(clauses[i].args[0]))

        elif isinstance(clauses, str):
            clauses = clauses.replace('~', 'Not')
            if len(clauses) > 0:
                clauses = expr(clauses)

            try:
                clauses = conjuncts(clauses)
            except AttributeError:
                pass

        return clauses

    def relaxed(self):
        """
        Removes delete list from the action by removing all negative literals from action's effect
        """
        return Action(Expr(self.name, *self.args), self.precond,
                      list(filter(lambda effect: effect.op[:3] != 'Not', self.effect)))

    def substitute(self, e, args):
        """Replaces variables in expression with their respective Propositional symbol"""

        new_args = list(e.args)
        for num, x in enumerate(e.args):
            for i, _ in enumerate(self.args):
                if self.args[i] == x:
                    new_args[num] = args[i]
        return Expr(e.op, *new_args)

    def check_precond(self, kb, args):
        """Checks if the precondition is satisfied in the current state"""

        if isinstance(kb, list):
            kb = FolKB(kb)
        for clause in self.precond:
            if self.substitute(clause, args) not in kb.clauses:
                return False
        return True

    def act(self, kb, args):
        """Executes the action on the state's knowledge base"""

        if isinstance(kb, list):
            kb = FolKB(kb)

        if not self.check_precond(kb, args):
            raise Exception('Action pre-conditions not satisfied')
        for clause in self.effect:
            kb.tell(self.substitute(clause, args))
            if clause.op[:3] == 'Not':
                new_clause = Expr(clause.op[3:], *clause.args)

                if kb.ask(self.substitute(new_clause, args)) is not False:
                    kb.retract(self.substitute(new_clause, args))
            else:
                new_clause = Expr('Not' + clause.op, *clause.args)

                if kb.ask(self.substitute(new_clause, args)) is not False:
                    kb.retract(self.substitute(new_clause, args))

        return kb


def monkey_banana():
    return PlanningProblem(initial='MonoEn(A) & NivelMono(abajo) & CajaEn(C) & BananasEn(B)', 
                           goals='MonoTiene(bananas)',
                           actions=[Action('Ir(x, y)',
                                           precond='MonoEn(x) & NivelMono(abajo)',
                                           effect='~MonoEn(x) & MonoEn(y)',
                                           domain='Posicion(x) & Posicion(y)'),
                                    Action('Trepar(x)',
                                           precond='MonoEn(x) & NivelMono(abajo) & CajaEn(x)',
                                           effect='~NivelMono(abajo) & NivelMono(arriba)',
                                           domain='Posicion(x)'),
                                    Action('Bajarse(x)',
                                           precond='MonoEn(x) & NivelMono(arriba) & CajaEn(x)',
                                           effect='~NivelMono(arriba) & NivelMono(abajo)',
                                           domain='Posicion(x)'),
                                    Action('LLevarCaja(x,y)',
                                           precond='MonoEn(x) & NivelMono(abajo) & CajaEn(x)',
                                           effect='~CajaEn(x) & CajaEn(y) & ~MonoEn(x) & MonoEn(y)',
                                           domain='Posicion(x) & Posicion(y)'),
                                    Action('TomarBananas(x)',
                                           precond='MonoEn(x) & NivelMono(arriba) & BananasEn(x) & CajaEn(x)',
                                           effect='MonoTiene(bananas)',
                                           domain='Posicion(x)'),],
                           domain='Posicion(A) & Posicion(B) & Posicion(C)')


def air_cargo():
    return PlanningProblem(initial='CargoAt(C1, SFO) & CargoAt(C2,JFK) & PlaneAt(P1, SFO) & PlaneAt(P2, JFK)',
                            goals='CargoAt(C1,JFK) & CargoAt(C2,SFO)',
                            actions=[Action('Load(c,p,a)',
                                             precond='CargoAt(c,a) & PlaneAt(p,a)',
                                             effect= '~CargoAt(c,a) & CargoIn(c,p)',
                                             domain='Cargo(c) & Plane(p) & Airport(a)'),
                                    Action('Unload(c,p,a)',
                                             precond='CargoIn(c,p) & PlaneAt(p,a)',
                                             effect='CargoAt(c,a) & ~CargoIn(c,p)',
                                             domain='Cargo(c) & Plane(p) & Airport(a)'),
                                    Action('Fly(p,f,t)',
                                            precond='PlaneAt(p,f)',
                                            effect= '~PlaneAt(p,f) & PlaneAt(p,t)',
                                            domain='Plane(p) & Airport(f) & Airport(t)'),
                                    ],
                                domain='Cargo(C1) & Cargo(C2) & Plane(P1) & Plane(P2) & Airport(JFK) & Airport(SFO)')

def spare_tire():
    
    return PlanningProblem(initial= 'At(Flat, Axle) & At(Spare,Trunk)',
                            goals='At(Spare,Axle)',
                            actions=[Action('Remove(obj, loc)',
                                            precond='At(obj,loc)',
                                            effect='~At(obj,loc) & At(obj,Ground)'),
                                    Action('PutOn(t, Axle)',
                                            precond=' At(t, Ground) & ~At(Flat,Axle) & ~At(Spare,Axle)',
                                            effect='~At(t, Ground) & At(t, Axle)',
                                            domain='Tire(t)'),
                                    Action('LeaveOvernight()',
                                            precond='',                                        
                                            effect='~At(Spare,Ground) & ~At(Square,Axle) & ~At(Spare, Trunk) & ~At(Flat, Ground) & ~At(Flat, Axle) & ~At(Flat, Trunk)'),

                            ],
                            domain= 'Tire(Flat) & Tire(Spare)'                     
                            )     

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
                            domain='Block(A) & Block(B) & Block(C) & Block(D) & Block(E) & Block(F) & Block(G) & Block(H) & Block(I) & Block(J) & Block(F) &  Block(G) & Block(Deposit) & Vehicle(V)  & Stop(E) & Stop(C) & End(G) & Semaphore(B) & Semaphore(D) & Semaphore(C) & Authority(B) & Authority(F)')
                                              


def get_solution(problem):
    solution = uniform_cost_search(ForwardPlan(problem)).solution()
    solution = list(map(lambda action: Expr(action.name, *action.args), solution))
    return solution

get_solution(VehicleActions())

import random as rn
import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self, distances, n_ants, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            print (shortest_path)
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path            
            self.pheromone = self.pheromone * self.decay            
        return all_time_shortest_path

    def spread_pheronome(self, all_paths):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:1]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)

        norm_row = row / row.sum()
        move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move


class SimulatedAnnealing(object):

    def __init__(self, distances, n_iterations, a = 0.99, t_0= 10**9):
        self.distances  = distances
        self.n_iterations = n_iterations
        self.a = a
        self.t_0 = t_0
        
    def run(self):
        current_path = self.gen_random_path()
        all_time_shortest_path = ("placeholder", np.inf)
        t = self.t_0
        
        for i in range(self.n_iterations):
            next_path = self.succesor(current_path)
            print(next_path)
            if self.path_dist(current_path) < all_time_shortest_path[1]:
                all_time_shortest_path = (current_path, self.path_dist(current_path)) 
            
            if self.acceptance_probability(self.path_dist(current_path), self.path_dist(next_path), t) >= random.random():
                path = next
                
            t = self.temperature(t)
            
            print(i, "best_solution: ", all_time_shortest_path)
            
        return all_time_shortest_path
    
    def path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_random_path(self):
        not_visited = np.arange(0,len(self.distances),1)
        print(not_visited)
        start = random.randint(0,len(self.distances)-1)
        not_visited = np.delete(not_visited,start)
        prev = start
        path =[]
        for i in range(len(self.distances) - 1):
            index = random.randint(0,len(not_visited)-1)
            move = not_visited[index]
            path.append((prev, move))
            prev = move
            not_visited = np.delete(not_visited,index)
        path.append((prev, start)) # going back to where we started

        return path
               
                         
    def temperature(self, t):
        return t * self.a
                         
    def acceptance_probability(self, current_dist, next_dist, temp):
        if current_dist > next_dist:
            return 1.0
        return (math.exp((current_dist-next_dist)/temp))

    
    def succesor(self, path):
        next_path = []
        current_path = []
        for elem in path:
            current_path.append(elem[0])
        swap_elements= random.sample(current_path,k=2)
        temp = current_path[swap_elements[0]]
        current_path[swap_elements[0]]=current_path[swap_elements[1]]
        current_path[swap_elements[1]]=temp

        for i in range(len(current_path)-1):
            next_path.append((current_path[i],current_path[i+1]))
        next_path.append((current_path[len(current_path)-1], current_path[0]))

        return next_path

distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

sa = SimulatedAnnealing(distances, 100)
#sa.run()

#ant_colony = AntColony(distances, 1, 100, 0.95, alpha=1, beta=1)
#shortest_path = ant_colony.run()
#print ("shorted_path: {}".format(shortest_path))
print(len(distances))

#print(get_solution(spare_tire()))