import networkx as nx
import matplotlib.pyplot as plt
import random

numbers = [i for i in range(1,16)]
random_tuple = random.sample(numbers, 2)
print(numbers)
print(random_tuple)

# Creamos un grafo vacío
G = nx.Graph()

# Añadimos algunos nodos y aristas
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_edge(1, 2)
G.add_edge(2, 3)

# Dibujamos el gráfico
#nx.draw(G)
#plt.show()

# Obtenemos la matriz de adyacencia del grafo
A = nx.to_numpy_matrix(G)

#print(A)

# Obtenemos la lista de adyacencia del grafo
L = nx.to_dict_of_lists(G)

#print(L)