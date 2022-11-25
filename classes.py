import numpy as np

class Graph:
    """Represents the map with the routes through which the vehicles will transit"""

    def __init__(self, rows, columns):
        self.map = np.array([[0 for i in range(columns)] for j in range(rows)]) 
        self.routes=[]
        self.authorities=[]

    def insert_route(self, route):
        self.routes.append(route)

    def insert_authority(self, id_authority, location):
        self.authorities.append(location)

    def insert_client(id_client, location):
        pass

    def insert_stop(self,location):
        pass

    def assign_vehicle_to_route(id_vehicle, id_route):
        pass
        

class Route:
    """Represents the path of the map that the vehicle takes to transport product"""

    def __init__(self, id):
        self.id=id
    
    def create_route(list):
        # verify list is a secuence of positions in a matrix 
        pass
        
        
class Authority:
    """Represents the traffic authorities """

    def __init__(self, id):
        self.id = id
        

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

    def __init__(self, id, capacity):
        self.id = id
        self.capacity=capacity
                    

class Client:
    """Represents the clients of the company"""

    def __init__(self, id):
        self.id=id

class Person:
    """Represents the person that the vehicle transports"""

    def __init__(self, id):
        self.id = id
        




