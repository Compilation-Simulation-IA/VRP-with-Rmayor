from geopy.geocoders import Nominatim, options
import pandas as pd
import math
import queue
import osmium
#from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
                       )
import networkx as nx

# Leer el archivo .pbf
with open('cuba-latest.osm.pbf', 'rb') as f:
    data = f.read()
import osmium

class NodeHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

    def node(self, n):
        self.nodes.append(n)

    def way(self, w):
        self.edges.extend(list(w.nodes))

# handler = NodeHandler()
# handler.apply_file("cuba-latest.osm.pbf")

# nodes = handler.nodes
# edges = handler.edges
def get_nodes_edges_from_pbf(file_path):
    handler = NodeHandler()
    handler.apply_file(file_path)
    nodes = {}
    edges = []
    for node in handler.nodes:
        nodes[node.id] = (node.lon, node.lat)
    for way in handler.ways:
        if "highway" in way.tags:
            for i in range(len(way.nodes) - 1):
                source = way.nodes[i]
                target = way.nodes[i + 1]
                edges.append((source, target))
    return nodes, edges

nodes, edges = get_nodes_edges_from_pbf("cuba-latest.osm.pbf")
print(nodes)
print(edges)
# # Crear un grafo vacío
G = nx.Graph(nodes,edges)

# Recorrer cada nodo del archivo .pbf y agregarlo al grafo
for node in data.nodes():
    G.add_node(node.id, attr_dict=node.tags)

# Recorrer cada arco del archivo .pbf y agregarlo al grafo
for way in data.ways:
    for i in range(len(way.nodes) - 1):
        G.add_edge(way.nodes[i], way.nodes[i+1], attr_dict=way.tags)

# df2 = pd.DataFrame({'Location':
#                     ['2094 Valentine Avenue,Bronx,NY,10457',
#                      '1123 East Tremont Avenue,Bronx,NY,10460',
#                      '412 Macon Street,Brooklyn,NY,11233']})

# df2[['location_lat', 'location_long']] = df2['Location'].apply(
#     geolocator.geocode).apply(lambda x: pd.Series(
#         [x.latitude, x.longitude], index=['location_lat', 'location_long']))


options.default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"

geocoder = Nominatim()

address = "156A, #107, Playa, La Habana, Cuba"

location = geocoder.geocode(address)

df2 = pd.DataFrame({'Location':
                    ['156A, #107, Playa, La Habana, Cuba',
                     '38 y 5ta A,Playa,La Habana,Cuba',
                     '23 y M, Vedado, La Habana, Cuba',
                     '23 y G, Vedado, La Habana, Cuba',
                     'Migas, Calle 17, RadioCuba, El Vedado, Plaza de la Revolución, La Habana, Plaza de la Revolución, 10424, Cuba']})

df2[['location_lat', 'location_long']] = df2['Location'].apply(
    geolocator.geocode).apply(lambda x: pd.Series(
        [x.latitude, x.longitude], index=['location_lat', 'location_long']))

latitude = location.latitude
longitude = location.longitude
print(df2.head())
print(latitude, longitude)

import folium

# Crea un mapa centrado en las coordenadas (latitud, longitud)
mapa = folium.Map(location=[23.12002,-82.38304],zoom_start=14,zoom_control=False)

for i in range (0,len(df2['Location'])):
    folium.Circle(location=(df2['location_lat'][i], df2['location_long'][i])).add_to(mapa)

# Muestra el mapa en una ventana emergente
mapa.save('mapa.html')