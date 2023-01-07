import pulp

# Creamos un diccionario que asigna a cada vehículo su capacidad máxima de carga y velocidad media
vehicles = {
    "vehiculo1": (50, 40),
    "vehiculo2": (30, 50),
    "vehiculo3": (40, 45)
}

# Creamos una lista de destinos, con la distancia en km desde el origen y la cantidad de paquetes a entregar
destinos = [
    ("destino1", 100, 15),
    ("destino2", 50, 10),
    ("destino3", 120, 20)
]

# Creamos el modelo de programación lineal
model = pulp.LpProblem("Tiempo de entrega de paquetes", pulp.LpMinimize)

# Creamos las variables del modelo, una por cada vehículo
tiempos = {vehiculo: pulp.LpVariable(f"Tiempo_{vehiculo}", lowBound=0, cat="Continuous") for vehiculo in vehicles}

# Establecemos la función objetivo como la suma de los tiempos de entrega de todos los vehículos
model += sum(tiempos.values())

# Agregamos una restricción para cada destino, indicando que la cantidad de paquetes entregados
# debe ser igual o mayor a la demanda de paquetes en ese destino
for destino, distancia, demanda in destinos:
    model += sum(vehicles[v][0] * tiempos[v] / vehicles[v][1] for v in vehicles) >= demanda

# Resolvemos el problema y obtenemos la solución óptima
model.solve()

# Imprimimos el tiempo de entrega de cada vehículo
for vehiculo, tiempo in tiempos.items():
    print(f"{vehiculo}: {tiempo.value()} horas")