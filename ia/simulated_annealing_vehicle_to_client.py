import random
from math import exp
from simulated_annealing import SimulatedAnnealing


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
                         
   





 #Example
#vehicle_capacities = [5,5,10,8,8]
#client_demands = [11,6,10]
#V = [1, 2, 3, 4,5]
#x, cost = simulated_annealing(vehicle_capacities, client_demands)
#print(check_constraint(x,vehicle_capacities,client_demands,True))
#print(f"The solution is: x = {x}, cost = {cost}")
