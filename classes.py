import numpy as np

class Graph:
    """Represents the map with the routes through which the vehicles will transit"""

    def __init__(self, rows, columns):
        self.map = np.array([[0 for i in range(columns)] for j in range(rows)]) 
        self.routes=[] #lista de listas de stops, una lista de stops es una ruta.
        self.authorities=[]
        self.vehicles = [] #lista de listas de vehiculos
        #lista de rutas cada elemt contiene una lista de tuplas (id_route, count_person).
        #Asi obtenemos la cantidad de personas en cada parada que conforman una ruta
        self.person_for_stop = [] 
        self.clients = []
        self.currents = [] # posicion actual de los vehiculos( representa un entero)
        self.Arrived = [] #la cantidad de arrivos es igual a la cantidad de clientes q tenga la empresa
        self.Departure = [] # misma idea de Arrived

    def insert_route(self, route):
        self.routes.append(route)

    def insert_authority(self, id_authority, location):
        self.authorities.append(location)

    #un cliente es una compañia que solicita los servicios de transporte de nuestra compañia
    def insert_client(id_client, location ):
        self.clients.append((id_client,location))

        #añadir una parada a la ruta especificada
    def insert_stop(self,route_id, location):
        self.routes[route_id].append(location)
    
    # insertar 1 o varias personas a una parada de una ruta especifica
    def insert_person(self, count_person, stop):
        pass

    def drive_next_stop(self, id_vehicle,id_route):
        """ Moves to the next stop until Arrived at the end """
        actual_pos = self.currents[id_vehicle]
        if actual_pos is self.Arrived[id_route]:
            return 1 #Llego con exito a su destino

        self.currents[id_vehicle] = self.routes[id_route][actual_pos + 1]


    #start =(x1,y1) , end = (x2,y2)
    def get_distance(self, start, end):
        """Return distance between current and next position in the route"""
        x_squared = pow((start[0] - end[0]), 2)
        y_squared = pow((start[1] - end[1]), 2)

        return sqrt(x_squared + y_squared)

    def assign_vehicle_to_route(id_vehicle, id_route):
        self.vehicles[id_route].append(id_vehicle)
        
class Route:
    """Represents the path of the map that the vehicle takes to transport product"""
    
    def __init__(self, id):
        self.id=id
        self.stops = []
    
    def create_route(stops):
        # verify list is a secuence of positions in a matrix 
        self.stops = stops

# Añadir una nueva parada a la ruta
    def add_stop(self, index_pos, stop):
        if stop not in self.stops:
            self.stops.insert(index_pos,stop)

#Eliminar una parada de la ruta
    def remove_depot_stop(self, depot_stop):
        self.depot_stops.remove(depot_stop)


class Stop:
    def __init__(self, id_route, x_axis, y_axis, person_list = [], time_waiting = 0):
        self.id_route = id_route
        self.person_list = person_list #lista de la clase person
        self.time_waiting = time_waiting #time_waiting es en minutos
        self.coordinates = (x_axis, y_axis)

    def __repr__(self):
        return f"<Stop: Coordinates {self.coordinates} in Route : {self.id_route}>"

    def __str__(self):
        return f"S({self.coordinates})"

    def increase_wait(self, minutes):
        self.time_waiting += minutes

    def decrease_wait(self, minutes):
        self.time_waiting = max(self.time_waiting - minutes, 0)

    def add_person_to_stop(new_person):
        self.person_list.append(new_person)
    
    def delete_person(old_person):
        self.person_list.remove(old_person)
        
class Authority:
    """Represents the traffic authorities """
 #position: posicion i,j de la autoridad del transito en la matriz
    def __init__(self, id, position):
        self.id = id
        self.position = position
        

class Company:
    """Represents the transport company"""

    def __init__(self, id):
        self.id = id
        self.clients=[]
        self.vehicles=[] #lista de vehiculos q tiene la compañia
        # una lista de listas de vehiculos. Cada indice representa el cliente y
        #  los vehiculos q tiene contratado
        self.assigned_vehicles = [] 

    def buy_vehicle(self, new_vehicle):
        self.vehicles.append(new_vehicle)
    
    def delete_vehicle(self, old_vehicle):
        self.vehicles.remove(old_vehicle)
    
    def add_client(self, new_client):
        self.clients.append(new_client)

    def assign_vehicle(self,id_client,id_vehicle):
        self.assigned_vehicles[id_client].append(id_vehicle)
        
class Vehicle:
    """Represents the vehicles of the company"""

    def __init__(self, id, capacity, state_of_live):
        self.id = id
        self.capacity = capacity
        self.state_of_life = state_of_live
                    

class Client:
    """Represents the clients of the company"""

    def __init__(self, id, company):
        self.id=id
        self.route = []
        self.company = company

class Person:
    """Represents the person that the vehicle transports"""

    def __init__(self, id, stop, client):
        self.id = id
        self.stop = stop
        self.client = client

    def __repr__(self):
        return f"<Person:{self.id}, Stop:{self.stop} , Client:{self.client}>"

    def __str__(self):
        return f"P({self.id})"