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
        self.currents = [] # posicion actual de los vehiculos
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
        if self.currents[id_vehicle] is self.Arrived[id_route]:
            return 1 #Llego con exito a su destino

        #next_stop = ME QUEDE AQUI
        

    def get_distance(self, start, end):
        pass

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
        self.vehicles=[]

    def add_vehicle(self, new_vehicle):
        self.vehicles.append(new_vehicle)
    
    def add_client(self, new_client):
        self.clients.append(new_client)

    
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