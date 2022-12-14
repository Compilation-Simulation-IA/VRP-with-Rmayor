import clases
import random
import math

# client: numero de clientes
# vehicle: lista de vehiculos q pide el cliente
# Departure: De donde sale el vehiculo
# Arrival: lugar a donde tiene q llegar el vehiculo
# stops: lista de paradas(contiene a Departure al principio y Arrival al final )
def simulate(client, vehicle, routes):
    Goblal_Time = 0
    Actual_State = routes.stops #Departure
    index = 0
    while Actual_State != Arrival:
        a,b = get_distance(stops[index], stops[index + 1])
        route_time = generateUniform(a, b)
        embark_time = generateUniform(3, 5) #tiempo mientras se van montando las personas al carro
        Goblal_Time += route_time

        Actual_State += 1

#recibe una lista de capacidades, q son las q tendran los vehiculos creados
def create_vehicules(capacity_list):
    vehicle_list = []
    for value, index in enumerate(capacity_list):
        v = Vehicle(index, value, 10)

def get_distance(start, end):
    pass

def generateExponential(lambda_value):
    return -(lambda_value * math.log(random.random()))

def generateUniform(a,b):
    if a<=b :
        return random.uniform(a,b)
    raise Exception("Invalid argument")

Map = Graph(5,5)
r1 = Route(id = 1)
#posiciones de la ruta, el 1er elem es la salida y el ultimo la llegada
r1.create_route([(1,1),(3,2),(4,4),(5,5)])
Map.insert_route(r1)
vehicle_list = create_vehicules([4])
