# VRP-IVNS

# Problema
El Problema de Enrutamiento de Vehículos (VRP, por sus siglas en inglés) es
un problema de optimización combinatoria que consiste en planificar recorridos
que permitan satisfacer las demandas de un conjunto de clientes geográficamente
dispersos. Para ello se cuenta con una flota de vehículos que parten desde uno
o varios depósitos centrales. El objetivo del VRP es diseñar rutas para cada
vehículo que minimicen o maximicen algún objetivo.
El VRP es un problema NP-duro, por lo que los métodos exactos solo son
factibles para resolver problemas de pequeña dimensión. Por ese motivo se han
desarrollado diferentes heurísticas y metaheurísticas para solucionarlos, entre
las que se encuentran las de búsqueda local.

# Inteligencia Artificial

Los algoritmos de búsqueda local son métodos en los que se define una solución
actual, una estructura de entorno, y de manera iterativa se generan soluciones
vecinas de la solución actual usando la estructura de entorno (o criterio de vecindad,
como también se les conoce). Las soluciones vecinas pueden reemplazar
o no a la solución actual en dependencia de su calidad para el problema de
optimización y del algoritmo en cuestión.
La metaheurística Búsqueda de Vecindad Variable (VNS) se diferencia de
otros algoritmos de búsqueda local por tener un conjunto finito de estructuras
de entornos que modifican secuencialmente la solución actual, hasta que ninguna
de ellas puede encontrar una solución mejor, y en ese caso se asume que la actual
es un óptimo del problema. Las ideas fundamentales de este algoritmo son que
un óptimo local para una estructura de entorno no tiene por qué serlo para otra
y que un óptimo local para todas las estructuras de entorno que se están usando
es un óptimo global, al menos, con respecto a ese conjunto de estructuras de
entorno.

El objetivo de este trabajo es modificar el algoritmo VNS para considerar
infinitos criterios de vecindad en el Problema de Enrutamiento de Vehóculos con
Restricciones de Capacidad.
Nota: Se puede utilizar una IA para la generación del lenguaje. También se
puede utilizar algoritmo evolutivo como variante de metaheurística.

# Compilación

Para poder considerar infinitos criterios de vecindad se construye el lenguaje
formal formado por todos los posibles criterios de vecindad que se pueden tener
para este problema, y cada vez que se “cambia de estructura de entorno” se
genera una nueva cadena del lenguaje, usando una gram´atica libre del contexto.
Las cadenas del lenguaje se pueden convertir en código ejecutable para que,
dada una solución, se pueda explorar su vecindad utilizando el criterio especificado por la cadena.

# Simulación

Se quiere simular el prblema anterior pero asociado al transporte de una empresa para sus trabajadores. 
Para ello se cuenta con una flota de carros, de distintos modelos, y varios almacenes. Los
carros salen de sus almacenes o parqueos, respectivamente. Estos siempre pasan por una ruta asociada a cada uno, la misma cada día.
Los vehículos, con el tiempo, se deterioran y necesitan mantenimiento, con lo
cual pasan a estar no disponibles, pero se mantienen en la plantilla de la empresa.
Hay un tiempo Ti en el cual el vehículo están en mantenimiento, el cual depende
del modelo del vehículo.
En la ruta de cada vehículo, en las paradas de trabajadores, hay una cantidad
máxima m de personas, de la cual el vehículo solo recoge k, donde k menor o igual que
m.

Se tienen vehículos de reserva a menos que el carro necesite mantenimiento, en cuyo caso se sustituye el
vehículo por otro en dependencia de las posibilidades de la empresa.

Se simula mover un cliente de una ruta a otra, reubicar un cliente en su misma ruta e intercambiar dos clientes para minimizar el costo del viaje. 
Existen diferentes criterios de vecindad que se simluarán a medida que se genere el lenguaje.
Cuando un carro no cubre su ruta porque esta en mantenimiento en el tiempo de comprar un nuevo carro, el carro mas cercano cubre la ruta de este.
La empresa cuenta con un monto inicial para la flota de vehiculos y destina en cada mes un presupuesto para ellos. 
Puede pasar que no hay presupuesto en un momento dado o es muy bajo y 
se escoge llevar a mantenimiento a un carro con el que se pierde dinero en vez de darlo de baja y comprar uno nuevo.
	
El objetivo de los vehiculos es cubrir la ruta, y se quiere disminuir el tiempo de las personas en la parada, 
el gasto de combustible y el tiempo de viaje de todos los trabajadores hasta la empresa.
