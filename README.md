# VRP with Rmayor 

# Problema
El Problema de Enrutamiento de Vehículos (VRP, por sus siglas en inglés) es un problema de optimización combinatoria que consiste en planificar recorridos que permitan satisfacer las demandas de un conjunto de clientes geográficamente dispersos. Para ello se cuenta con una flota de vehículos que parten desde uno o varios depósitos centrales. El objetivo del VRP es diseñar rutas para cada vehículo que minimicen o maximicen algún objetivo. El VRP es un problema NP-duro, por lo que los métodos exactos solo son factibles para resolver problemas de pequeña dimensión. Por ese motivo se han desarrollado diferentes heurísticas y metaheurísticas para solucionarlos.

Algunos de los factores que se deben tener en cuenta al resolver un VRP incluyen:

- El costo de los desplazamientos entre las diferentes ubicaciones: esto puede ser la distancia, el tiempo, el consumo de combustible, etc.

- La capacidad de carga de cada vehículo: cada vehículo solo puede llevar una cantidad limitada de carga.

- Las restricciones de tiempo: algunas entregas o recolecciones deben realizarse en un plazo de tiempo específico.

- Las restricciones de capacidad: algunas ubicaciones pueden tener una demanda máxima que no puede excederse.

Para resolver un VRP, se pueden utilizar diferentes métodos, como el algoritmo de ramificación y poda, los algoritmos genéticos, las colonias de hormigas, entre otros. Al combinar estos métodos con técnicas de compilación y simulación, se pueden obtener soluciones eficientes para problemas de tamaño moderado

 En este proyecto combinaremos los conocimientos de compilación, simulación e inteligencia artificial para resolver un subconjunto de estos problemas. 

# Inteligencia Artificial

La Inteligencia Artificial puede ser utilizada para resolver el Problema de Enrutamiento de Vehículos de diversas maneras. Algunas de las técnicas que se pueden utilizar incluyen:

Algoritmo A*: como mencioné anteriormente, este algoritmo puede ser utilizado para encontrar el camino más corto entre dos puntos en un grafo. En el caso del VRP, se puede utilizar A* para encontrar la ruta más corta entre el depósito y cada una de las ubicaciones de los clientes, y luego combinar las rutas encontradas para formar un plan de entrega o recolección.

Metaheurísticas: las colonias de hormigas y otros métodos basados en metaheurísticas pueden ser utilizados para encontrar soluciones aproximadas al VRP. Estos métodos suelen ser más eficientes que los métodos exactos para resolver problemas de mayor tamaño, pero tienen el inconveniente de que las soluciones obtenidas no siempre son óptimas.

Planificación: como mencioné anteriormente, la planificación puede ser utilizada para definir un conjunto de acciones para alcanzar un objetivo específico. En el caso del VRP, la planificación puede ser utilizada para definir un plan de entrega o recolección que cumpla con las demandas de los clientes de manera eficiente.

# Compilación

Un lenguaje de dominio específico (DSL, por sus siglas en inglés) es un lenguaje de programación diseñado para resolver problemas específicos de un dominio particular. En el caso del Problema de Enrutamiento de Vehículos, se puede crear un DSL para codificar los problemas y facilita la tarea de resolverlos utilizando algoritmos de optimización.

La compilación consiste en convertir el código escrito en un DSL en un lenguaje de programación más general, que puede ser ejecutado por una computadora. Esto permite que los problemas de enrutamiento de vehículos sean resueltos de manera eficiente utilizando algoritmos de optimización.

El lenguaje de dominio específico (DSL) creado para codificar problemas de enrutamiento de vehículos se puede conectar a la simulación para evaluar las soluciones propuestas y determinar cuál es la más adecuada. Esto permite que los problemas sean resueltos de manera más eficiente y permite predecir el comportamiento del sistema en diferentes escenarios.

Incluye sentencias de iteración para recorrer las diferentes rutas propuestas y compararlas entre sí. Esto permite evaluar las soluciones propuestas y determinar cuál es la más adecuada.

Además, el DSL compara múltiples parámetros, como el tiempo o el rendimiento de diferentes empresas que ofrecen servicios de enrutamiento de vehículos, etc.

En general, la creación de un DSL para codificar problemas de enrutamiento de vehículos puede ser beneficiosa porque permite que los problemas sean expresados de manera más clara y concisa, lo que facilita su resolución y permite a los usuarios trabajar con ellos de manera más eficiente. La conexión entre el DSL y la simulación  permite evaluar las soluciones propuestas de manera más precisa y predecir el comportamiento del sistema en distintas condiciones. Esto puede ser útil para tomar decisiones y optimizar el funcionamiento del sistema de enrutamiento de vehículos.

# Simulación

Se quiere simular el problema anterior pero asociado al transporte de una empresa para sus trabajadores.
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
	
El objetivo de los vehículos es cubrir la ruta, y se quiere disminuir el tiempo de las personas en la parada, 
el gasto de combustible y el tiempo de viaje de todos los trabajadores hasta la empresa.
