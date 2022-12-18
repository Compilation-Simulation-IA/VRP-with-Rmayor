from classes import Graph, Company, Person, Stop, Route, Vehicle, Client, Authority
import random
import math

class VRP_Simulation:
    def __init__(self, graph_map):
        self.graph_map = graph_map
        self.global_time = 0
        #Inicializar los currents de todas las rutas
        for index, r in enumerate(self.graph_map.routes):
            self.graph_map.currents.append(self.graph_map.routes[index].stops[0]) #Departure
            final = len(self.graph_map.routes[index].stops) - 1
            self.graph_map.target.append(self.graph_map.routes[index].stops[final])
        
        
    # Que comience la simulacion del vehiculo id_vehicle en la ruta id_routes
    def start(self, id_vehicle, id_route):
        Actual_State = self.graph_map.currents[id_route]
        Arrival = self.graph_map.target[id_route]
        local_time = 0
        
        while Actual_State != Arrival:
            print(f"Time: {self.global_time}")
            print(Actual_State)
            Actual_State, local_time = self.drive_next_stop(Actual_State, id_vehicle, id_route,local_time)
            self.global_time +=local_time
        print(f"El vehiculo llego al final de la ruta. Parada {Arrival}")

    def drive_next_stop(self,Actual_State, id_vehicle, id_route, local_time):
        """ Moves to the next stop until Arrived at the end """
        next_stop = self.graph_map.routes[id_route].stops[Actual_State.id + 1]
        distance = self.get_distance(Actual_State.coordinates,next_stop.coordinates )
        a, b = self.get_distance_time(distance)
        route_time = round(self.generateUniform(a, b))
        embark_time = self.get_embark_time(len(next_stop.person_list)) #tiempo mientras se van montando las personas al carro
        local_time += route_time

        print(f"El vehiculo {id_vehicle} de la ruta {id_route} se movio a la siguiente parada.")
        self.graph_map.currents[id_route] = next_stop
        print(f"El vehiculo {id_vehicle} llego a la parada {next_stop.id}.")

        return next_stop, local_time
    
    #start =(x1,y1) , end = (x2,y2)
    def get_distance(self, start, end):
        """Return distance between current and next position in the route"""
        x_squared = pow((start[0] - end[0]), 2)
        y_squared = pow((start[1] - end[1]), 2)

        return math.sqrt(x_squared + y_squared)

    def get_distance_time(self, distance):
        return 3,5
    
    def get_embark_time(self, person_count):
        a = max(3,person_count - 3)
        b = person_count + 3
        return self.generateUniform(a,b)

    def generateExponential(self, lambda_value):
        return -(lambda_value * math.log(random.random()))
    
    def generateUniform(self, a, b):
        if a <= b :
            return random.uniform(a,b)
        raise Exception("Invalid argument.")
    
city_map = Graph(5,5)
company = Company(0)
client = Client(0,(5,5))
vehicle = Vehicle(0, 4, 10)

company.add_client(client)
company.buy_vehicle(vehicle)
company.assign_vehicle(client, vehicle)

stop_list = []
coordinates = [(1,1), (2,3), (4,4), (5,5)]

for i in range(0,4):
    p = Person(i, client)
    s = Stop(i, coordinates[i][0], coordinates[i][1], [p], 3)
    stop_list.append(s)
    
route = Route(0,stop_list) 

city_map.insert_company(company)
city_map.insert_route(route)

vrp = VRP_Simulation(city_map)
vrp.start(0,0)
print("exito")
    