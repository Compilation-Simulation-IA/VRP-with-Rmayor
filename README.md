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
El lenguaje de dominio específico (DSL) creado para codificar problemas de enrutamiento de vehículos se puede conectar a la simulación para evaluar las soluciones propuestas y determinar cuál es la más adecuada. Esto permite que los problemas sean resueltos de manera más eficiente y permite predecir el comportamiento del sistema en diferentes escenarios.

Este lenguaje esta desarrollado en python, con una gramatica LALR. Para el desarrollo del compilador se usó PLY, que es una implementación de Python pura del
constructor de compilación lex/yacc. Incluye soporte al parser LALR(1) así como herramientas
para el análisis léxico de validación de entrada y para el reporte de errores. El análisis sintáctico se divide en 2 fases: en una se realiza el análisis léxico, con la construcción
de un lexer, y en la otra se realiza el proceso de parsing, definiendo la gramática e implementando un parser para la construcción del Árbol de Sintaxis Abstracta (AST).
El programa fuente se procesa de izquierda a derecha y se agrupan en componentes
léxicos (tokens) que son secuencias de caracteres que tienen un significado. Todos los espacios
en blanco, comentarios y demás información innecesaria se elimina del programa fuente. El
lexer, por lo tanto, convierte una secuencia de caracteres (strings) en una secuencia de tokens.

El parser también se implementó mediante PLY, especificando la gramática y las acciones para
cada producción. Para cada regla gramatical hay una función cuyo nombre empieza con p_. El
docstring de la función contiene la forma de la producción, escrita en EBNF. PLY usa los dos puntos (:) para separar la parte izquierda y la derecha de la producción gramatical. El símbolo del lado izquierdo de la primera función es considerado el símbolo
inicial. El cuerpo de esa función contiene código que realiza la acción de esa producción.
En cada producción se construye un nodo del árbol de sintaxis abstracta.

El procesador de parser de PLY procesa la gramática y genera un parser que usa el algoritmo de
shift-reduce LALR(1), que es uno de los más usados en la actualidad. Aunque LALR(1) no puede
manejar todas las gramáticas libres de contexto, la gramática usada fue refactorizada
para ser procesada por LALR(1) sin errores.

Para realizar los recorridos en el árbol de derivación se hace uso del patrón visitor. Este patrón nos permite abstraer el concepto de procesamiento de un nodo. Cada elemento del nodo se procesa y se envia a la simulacion para ejecutarla

Un ejemplo de la estructura que debe tener el programa es la siguiente. En mapa el usuario carga el mapa a simular, en stops se definen las paradas, en vehicle_type los tipos de vehiculos que se usan, en clients, cada una de las empresas clientes que van a simularse, en company se inicializa el presupuesto, la cantidad de vehiculos y el deposito y en demandas se definen funciones, variables y se Simula el proceso de la aplicacion

{
	
	map 
	{
		import "mapa.txt"
	}

	stops 
	{
    		s1 (address:"156A, #107, Playa, La Habana, Cuba", people:5)
	}

	vehicle_type 
	{
    		small (miles: 40000, capacity: 30)
    		medium (miles: 40000, capacity: 70)
	}

	clients 
	{
    		c1 (name: "Coca Cola", stops_list: (s1),depot:s1 ) (*puede cambiarse por []*)
	}
	
	company 
	{
    		budget: 1000000
    		depot (address:"156A, #107, Playa, La Habana, Cuba")
    		small v1: 5
    		medium v2: 3
	}
	
	demands
	{
		func print() : IO 
		{
			out_string("reached!!\n")
	        }

		func main(): Object 
		{
        		print()
		}

    		test1<- 1

    		test3<- "1"
    
		Simulate
	}


Se provee al ususario una simple interfaz para escribir el codigo y ver el resultado de la simulacion
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
