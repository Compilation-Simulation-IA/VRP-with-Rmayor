import numpy as np

class Graph:
    """Represents the map with the routes through which the vehicles will transit"""

    def __init__(self, rows, columns):
        self.map = np.array([[0 for i in range(columns)] for j in range(rows)]) 
        self.routes=[] #lista de rutas, cada objeto es una ruta q contiene una lista de stops.
        self.authorities=[]
        self.vehicles = [] #diccionario: key=ruta, value=lista de vehiculos
        #lista de rutas cada elemt contiene una lista de tuplas (id_route, count_person).
        #Asi obtenemos la cantidad de personas en cada parada que conforman una ruta
        self.person_for_stop = [] 
        self.clients = []
        self.currents = [] # posicion actual de los vehiculos( representa un entero)
        self.target = [] #lista de objetivos finales de cada ruta
        self.Arrived = [] #la cantidad de arrivos es igual a la cantidad de Clientes-Compañias q tenga la empresa
        self.Departure = [] # misma idea de Arrived

    def insert_company(self,company):
        self.company = company

    def insert_route(self, route):
        self.routes.append(route)

    def insert_authority(self, id_authority, location):
        self.authorities.append(location)

    #un cliente es una compañia que solicita los servicios de transporte de nuestra compañia
    def insert_client(id_client, location ):
        self.clients.append(id_client)

        #añadir una parada a la ruta especificada
    def insert_stop(self,id_route, location):
        self.routes[id_route].append(location)
    
    # insertar 1 o varias personas a una parada de una ruta especifica
    def insert_person(self, count_person, stop):
        pass

    def assign_vehicle_to_route(id_vehicle, id_route):
        self.vehicles[id_route.id].append(id_vehicle)
        
class Route:
    """Represents the path of the map that the vehicle takes to transport product"""
    
    def __init__(self, id, stops = []):
        self.id=id
        self.stops = []
        if len(stops) != 0:
            for s in stops:
                self.append_stop(s)
        
    
    def __repr__(self):
        return f"<Route: ID {self.id}, Stop Total Count: {len(self.stops)}>"

    def create_route(stops):
        # verify list is a secuence of positions in a matrix 
        self.stops = stops

# Añadir una nueva parada a la ruta en una posicion especifica
    def insert_stop(self, stop, index_pos ):
        if stop not in self.stops:
            self.stops.insert(index_pos,stop)
            stop.set_stop_to_route(self)
            sorted(self.stops)

# Añadir una nueva parada al final de la ruta
    def append_stop(self,stop):
        if stop not in self.stops:
            self.stops.append(stop)
            stop.set_stop_to_route(self)

#Eliminar una parada de la ruta
    def remove_depot_stop(self, depot_stop):
        self.depot_stops.remove(depot_stop)


class Stop:
    def __init__(self, id, x_axis, y_axis,person_list, time_waiting = 0 ):
        self.id = id
        self.person_list = []
        if len(person_list) != 0:
            for p in person_list:
                self.add_person_to_stop(p)

        self.time_waiting = time_waiting #time_waiting es en minutos
        self.coordinates = (x_axis, y_axis)

    def __repr__(self):
        return f"<Stop: ID {self.id}:Coordinates {self.coordinates} in Route : {self.id_route}>"

    def __str__(self):
        return f"Stop{self.coordinates}"

    def __gt__(self, other_stop):
        return self.id > other_stop.id

    def increase_wait(self, minutes):
        self.time_waiting += minutes

    def decrease_wait(self, minutes):
        self.time_waiting = max(self.time_waiting - minutes, 0)

    def add_person_to_stop(self, new_person):
        self.person_list.append(new_person)
        new_person.set_stop = self
    
    def delete_person(self, old_person):
        self.person_list.remove(old_person)

    def set_stop_to_route(self, id_route):
        self.id_route = id_route
        
class Authority:
    """Represents the traffic authorities """
 #position: posicion i,j de la autoridad del transito en la matriz
    def __init__(self, id, position):
        self.id = id
        self.position = position
        
    def __repr__(self):
        return f"<Authority: ID {self.id}, Position: {self.position}>"
class Company:
    """Represents the transport company"""

    def __init__(self, id):
        self.id = id
        self.clients=[]
        self.vehicles=[] #lista de vehiculos q tiene la compañia
        # una lista de listas de vehiculos. Cada indice representa el cliente y
        #  los vehiculos q tiene contratado
        self.assigned_vehicles = {} 

    def __repr__(self):
        return f"<Company: ID {self.id}>"

    def buy_vehicle(self, new_vehicle):
        self.vehicles.append(new_vehicle)
    
    def delete_vehicle(self, old_vehicle):
        self.vehicles.remove(old_vehicle)
    
    def add_client(self, new_client):
        self.clients.append(new_client)

    def assign_vehicle(self,id_client,id_vehicle):
        self.assigned_vehicles[id_client] = id_vehicle

class Vehicle:
    """Represents the vehicles of the company"""

    def __init__(self, id, capacity, state_of_live):
        self.id = id
        self.capacity = capacity
        self.state_of_life = state_of_live

    def __repr__(self):
        return f"<Vehicle: ID {self.id}, Capacity: {self.capacity}, State of Live: {self.state_of_life}>" 

class Client:
    """Represents the clients of the company"""

    def __init__(self, id,location):
        self.id=id
        self.location = location
        self.route = [] #lista de rutas del cliente compañia
        self.vehicles = []

    def __repr__(self):
        return f"<Client: ID {self.id}>"
    #def add_vehicle()
    
class Person:
    """Represents the person that the vehicle transports"""

    def __init__(self, id, client_Company):
        self.id = id
        self.client_Company = client_Company

    def set_stop(self,stop):
        self.stop = stop

    def __repr__(self):
        return f"<Person:{self.id}, Stop:{self.stop} , Client Company:{self.client_Company}>"

    def __str__(self):
        return f"P({self.id})"