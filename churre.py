import constraint

# Definimos un diccionario que asocia a cada vehículo su capacidad
capacities = {'vehicle1': 10, 'vehicle2': 8, 'vehicle3': 6}
routes=['r1','r2','r3']
# Definimos un diccionario que asocia a cada parada el número de personas que hay
stops = {'stop1': 5, 'stop2': 7, 'stop3': 3}

# Definimos una matriz de distancias entre paradas y almacenes
distances = {
    'stop1': {'stop2': 2, 'stop3': 3},
    'stop2': {'stop1': 2,'stop3':4},
    'stop3': {'stop1': 3, 'stop2':4}
}

# Creamos un nuevo problema
problem = constraint.Problem()

# Añadimos las variables del problema (una por cada parada)
class RouteDomain(constraint.Domain):
    def __init__(self, routes):
        self.routes = routes

    def __contains__(self, value):
        return value in self.routes

# Añadimos las variables del problema (una por cada parada)
for stop in stops:
    problem.addVariable(stop, constraint.Domain(routes))

# Añadimos la restricción de que cada parada sólo puede estar en una ruta
problem.addConstraint(constraint.AllDifferentConstraint())

# Añadimos la restricción de que la distancia total de cada ruta debe ser mínima
class MinDistanceConstraint(constraint.Constraint):
  def __init__(self, distances):
    self.distances = distances

  def isSatisfied(self, assignments):
    stop1 = assignments['stop1']
    stop2 = assignments['stop2']
    stop3 = assignments['stop3']
    return min([self.distances[stop1][stop2], self.distances[stop1][stop3], self.distances[stop2][stop3]])

for vehicle in capacities:
  problem.addConstraint(MinDistanceConstraint(distances), stops)

# Resolvemos el problema
solutions = problem.getSolutions()

# Procesamos la solución
for solution in solutions:
  # Obtener la ruta asignada a cada vehículo
  rutas = {}
  for vehicle in capacities:
    rutas[vehicle] = [solution[stop] for stop in solution if solution[stop] == vehicle]

  # Calcular la distancia total recorrida por cada ruta
  for vehicle in rutas:
    distancia = 0
    for i in range(len(rutas[vehicle]) - 1):
      distancia += distances[rutas[vehicle][i]][rutas[vehicle][i+1]]
    print(f" {solution}")