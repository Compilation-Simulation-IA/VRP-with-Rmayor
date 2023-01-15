import random
from math import exp



class SimulatedAnnealing():

    def __init__(self, vehicle_capacities, client_demands, T_0=100, T_min=0.0001, alpha=0.95, max_iter=100):
        self.vehicle_capacities  = vehicle_capacities
        self.client_demands = client_demands
        self.max_iter = max_iter
        self.alpha = alpha
        self.T_0 = T_0
        self.T_min = T_min
        
    def run(self):
            
        # Initial solution
        x = self.gen_random_path()
        current_cost = self.cost(x)
        T = self.T_0
        for i in range(self.max_iter):
            # Generate a random neighbor
            new_x = self.succesor(x)
            new_cost = self.cost(new_x)

            # Check if the neighbor is better than the current solution

            delta = new_cost - current_cost
            if delta < 0 or random.uniform(0, 1) < exp(-delta / T):
                x = new_x
                current_cost = new_cost
            T = self.temperature(T)
            if T < self.T_min:
                break

        return x, current_cost
        
       
    def gen_random_path(self):
        
        x = [random.randint(0, 1) for i in range(len(self.vehicle_capacities) * len(self.client_demands))]

        while not self.check_constraint(x):
            x = [random.randint(0, 1) for i in range(len(self.vehicle_capacities) * len(self.client_demands))]

        return x
      
       
    def succesor(self, current_solution):
        new_x = current_solution.copy()
        random_index = random.randint(0, len(self.vehicle_capacities) * len(self.client_demands)-1)
        new_x[random_index] = 1 - new_x[random_index]
        i = 50

        while not self.check_constraint(new_x):
            new_x[random_index] = 1 - new_x[random_index]
            random_index = random.randint(0, (len(self.vehicle_capacities) * len(self.client_demands))-1)
            new_x[random_index] = 1 - new_x[random_index]
            if i < 0:
                return current_solution
            i-=1

        return new_x       

    def temperature(self, t):
        return t * self.alpha

class SimulatedAnnealingVehiclesToClients(SimulatedAnnealing):

    def __init__(self, vehicle_capacities, client_demands, T_0=100, T_min=0.0001, alpha=0.95, max_iter=100):
        super().__init__(vehicle_capacities, client_demands, T_0, T_min, alpha, max_iter)
        self.full = len(vehicle_capacities)-len(client_demands)>0

    def check_constraint(self, current_solution):

        for i in range(len(self.vehicle_capacities)):
            if sum(current_solution[i*len(self.client_demands):i*len(self.client_demands)+ len(self.client_demands)]) > 1:
                return False       

        s = 0
        sum_capacities = 0
        for i in range(len(self.client_demands)):
            for j in range(len(self.vehicle_capacities)):
                s += current_solution[i + j*len(self.client_demands)]
                sum_capacities += current_solution[i + j*len(self.client_demands)] * self.vehicle_capacities[j]

            if s == 0 or (self.full and sum_capacities < self.client_demands[i]):
                return False
            s = 0
            sum_capacities = 0
    
        return True

   
    def cost(self,current_solution):
        return sum([self.vehicle_capacities[i]*current_solution[i] for i in range(len(self.vehicle_capacities))]) - sum([self.client_demands[i] for i in range(len(self.client_demands))])

class SimulatedAnnealingRouteToVehicle(SimulatedAnnealing):

    def __init__(self, vehicle_capacities, client_demands, T_0=100, T_min=0.0001, alpha=0.95, max_iter=100):
        super().__init__(vehicle_capacities, client_demands, T_0, T_min, alpha, max_iter)
        
 
    def check_constraint(self, current_solution):

        s = 0
        
        # verificar que a todas las paradas se le asigna un vehiculo
        for i in range(len(self.client_demands)):
            for j in range(len(self.vehicle_capacities)):
                s += current_solution[i + j*len(self.client_demands)]                
            if s != 1:
                return False
            s =0

        # verificar que todos los vehiculos tienen los depositos
        for i in range(len(self.vehicle_capacities)):
            vehicle_vector = current_solution[i*len(self.client_demands):i*len(self.client_demands)+ len(self.client_demands)]
            if sum(vehicle_vector[len(vehicle_vector)-2:len(vehicle_vector)]) != 2:
                current_solution[i*len(self.client_demands) + len(vehicle_vector)-2:i*len(self.client_demands)+ len(self.client_demands)] = [1,1]    
                         
                

        return True

   

    def cost(self, current_solution):
        s = 0

        for i in range(len(self.vehicle_capacities)):
            for j in range(len(self.client_demands)):
                s += current_solution[i*len(self.client_demands)] * (self.vehicle_capacities[i] -self.client_demands[j])

        return s