import random
from math import exp
from simulated_annealing import (SimulatedAnnealing)


class SimulatedAnnealingRouteToVehicle(SimulatedAnnealing):

    def __init__(self, vehicle_capacities, client_demands, T_0=100, T_min=0.0001, alpha=0.95, max_iter=100):
        super().__init__(vehicle_capacities, client_demands, T_0, T_min, alpha, max_iter)
        
 
    def check_constraint(self, current_solution):

        for i in range(len(self.vehicle_capacities)):
            vehicle_vector = current_solution[i*len(self.client_demands):i*len(self.client_demands)+ len(self.client_demands)]
            if sum(vehicle_vector[:len(vehicle_vector)-2]) != 1 or sum(vehicle_vector[len(vehicle_vector)-2:len(vehicle_vector)]) != 2:               
                return False  

        return True

   

    def cost(self, current_solution):
        s = 0

        for i in range(len(self.vehicle_capacities)):
            for j in range(len(self.client_demands)):
                s += current_solution[i*len(self.client_demands)] * (self.vehicle_capacities[i] -self.client_demands[j])

        return s
                         