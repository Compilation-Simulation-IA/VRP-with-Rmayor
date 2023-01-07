import random

# Paradas disponibles
paradas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Capacidad de cada vehículo
capacity = [20, 20, 20, 20, 20]
actual_capacity = [20, 20, 20, 20, 20]
# Personas a recoger en cada parada
people = [10, 5, 4, 5, 8, 14, 3, 15, 7, 15]
actual_people = [10, 5, 4, 5, 8, 14, 3, 15, 7, 15]
# Distancias entre las paradas
distances = [[0, 10, 15, 20, 10, 10, 5, 19, 20, 20],
             [10, 0, 5, 10, 5, 8, 10, 12, 20, 11],
             [15, 5, 0, 5, 5, 8, 10, 12, 20, 11],
             [20, 10, 5, 0, 5, 50, 100, 12, 20, 11],
             [10, 5, 5, 5, 0, 3, 5, 7, 15, 6],
             [10, 8, 8, 50, 3, 0, 8, 8, 15, 8],
             [5, 10, 10, 100, 5, 8, 0, 10, 15, 10],
             [19, 12, 12, 12, 7, 8, 10, 0, 19, 12],
             [20, 20, 20, 20, 15, 15, 15, 19, 0, 19],
             [20, 11, 11, 11, 6, 8, 10, 12, 19, 0]]
             
initial_depot_distance = [10, 10, 10, 10, 15, 20, 10, 16, 10, 8]
final_depot_distance = [10, 10, 10, 10, 15, 20, 10, 16, 10, 8]

# Tamaño de la población
POP_SIZE = 100000


# Número máximo de iteraciones
MAX_ITER = 1000


def total_distance(ruta):
    # Inicializar la distancia máxima en 0
    total_distance = 0
    # Recorrer las paradas asignadas al vehículo
    if ruta == []:
        return 0
    if len(ruta) == 1:
        total_distance += initial_depot_distance[ruta[0]]
        total_distance += final_depot_distance[ruta[0]]
    else:
        for i in range(len(ruta) - 1):
            # Sumar la distancia entre la parada actual y la siguiente
            if i == 0:
                total_distance += initial_depot_distance[ruta[i]]
            total_distance += distances[ruta[i]][ruta[i+1]]
            if i == len(ruta) - 2:
                total_distance += final_depot_distance[ruta[i+1]]
    # Devolver la distancia máxima

    return total_distance


def eval_solution(solution):
    # Calcular la distancia máxima recorrida por cada vehículo
    new_distances = [total_distance(ruta) for ruta in solution]
    # Devolver la distancia máxima
    return sum(new_distances)


def generate_random_solution():
    actual_capacity = capacity.copy()
    actual_people = people.copy()
    # Crear la solución vacía
    solution = [[] for _ in range(len(capacity))]

    # Copiar las paradas disponibles
    remaining_paradas = paradas[:]
    # Mientras queden paradas sin asignar

    while remaining_paradas:
        change = False
        # Seleccionar un vehículo al azar
        vehiculo_index = random.randint(0, len(capacity)-1)
        vehiculo = solution[vehiculo_index]
        # Seleccionar una parada al azar de las que quedan
        parada = random.choice(remaining_paradas)
        if actual_people[parada] <= actual_capacity[vehiculo_index]:
            # Asignar la parada al vehículo seleccionado
            vehiculo.append(parada)
            actual_capacity[vehiculo_index] -= actual_people[parada]
            actual_people[parada] = 0
            change = True
            remaining_paradas.remove(parada)
        else:
            actual_people[parada] -= actual_capacity[vehiculo_index]
            # Eliminar la parada de las que quedan

        if not change:
            return None

    # Devolver la solución generada
    return solution


# Inicializar la población
pop = []
for _ in range(POP_SIZE):
    solution = generate_random_solution()
    if solution != None:
        pop.append(solution)

if pop != []:
    # Inicializar la mejor solución conocida
    best_solution = min(pop, key=eval_solution)
else:
    best_solution = ""
# Imprimir la mejor solución
print(best_solution)
