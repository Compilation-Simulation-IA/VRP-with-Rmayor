from shapely.geometry import Polygon
# Lectura datos osm
import osmium as osm

# Tratamiento de datos
import pandas as pd
import numpy as np
import itertools

# Tratamiento de datos geográficos y mapas
import matplotlib.pyplot as plt
#import geopandas as gpd
from geopy.distance import distance
from shapely.geometry import Polygon
import folium
from folium.plugins import HeatMap
from branca.element import Figure
class POIHandler(osm.SimpleHandler):
    '''
    Clase para extraer información de un archivo osm.pbf. Únicamente se extraen
    elementos identificados como 'node' o 'area'. Además, se puede aplicar un filtrado
    para seleccionar únicamente aquellos que tengan tags con un determinado key y
    value.
    
    La posición de las áreas se obtiene calculando el centroide del polígono que
    forman sus nodos.
    
    TODO: 'all' value to include all available values of a tag.
    
    Arguments
    ---------
    
    custom_filter: dict
        Diccionario con los tags y valores que han de tener los elementos para
        ser extraídos. Por ejemplo:
        
        `{'amenity': ['restaurant', 'bar']}` selecciona únicamente aquellos
        elementos que tengan el tag 'amenity' con valor 'restaurant' o 'bar'.
        
        `{'amenity': ['restaurant', 'bar'], 'building': ['car']}` selecciona
        únicamente aquellos elementos que tengan el tag 'amenity' con valor
        'restaurant' o 'bar', o los que tengan el tag 'building' con valor 'hotel'.
    '''
    
    def __init__(self, custom_filter=None):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        self.custom_filter = custom_filter
        
        if self.custom_filter:
            for key, value in self.custom_filter.items():
                if isinstance(value, str):
                    self.custom_filter[key] = [value]
             
    def node(self, node):
        if self.custom_filter is None:
            name = node.tags.get('name', '')
            self.tag_inventory(node, 'node', name)
        else:
            if any([node.tags.get(key) in self.custom_filter[key] for key in self.custom_filter.keys()]):
                name = node.tags.get('name', '')
                self.tag_inventory(node, 'node', name)
    
    def way(self, way):
        if self.custom_filter is None:
            name = way.tags.get('name', '')
            self.tag_inventory(way, 'way', name)
        else:
            if any([way.tags.get(key) in self.custom_filter[key] for key in self.custom_filter.keys()]):
                name = way.tags.get('name', '')
                self.tag_inventory(way, 'way', name)

    def relation(self, relation):
        if self.custom_filter is None:
            name = relation.tags.get('name', '')
            self.tag_inventory(relation, 'relation', name)
        else:
            if any([relation.tags.get(key) in self.custom_filter[key] for key in self.custom_filter.keys()]):
                name = relation.tags.get('name', '')
                self.tag_inventory(relation, 'relation', name)
                
    # def area(self, area):
    #     if self.custom_filter is None:
    #         name = area.tags.get('name', '')
    #         self.tag_inventory(area, 'area', name)
    #     else:
    #         if any([area.tags.get(key) in self.custom_filter[key] for key in self.custom_filter.keys()]):
    #             name = area.tags.get('name', '')
    #             self.tag_inventory(area, 'area', name)

    def tag_inventory(self, elem, elem_type, name):
        if elem_type == 'node':
            for tag in elem.tags:
                self.osm_data.append([elem_type, 
                                       elem.id,
                                       name,
                                       elem.location.lon,
                                       elem.location.lat,
                                       pd.Timestamp(elem.timestamp),
                                       len(elem.tags),
                                       tag.k, 
                                       tag.v])
        elif elem_type == 'relation':
            for tag in elem.tags:
               self.osm_data.append([elem_type, 
                                   elem.id,
                                   name,
                                   pd.Timestamp(elem.timestamp),
                                   len(elem.tags),
                                   tag.k, 
                                   tag.v])
        elif elem_type == 'way':
            for tag in elem.tags:
                self.osm_data.append([elem_type, 
                                   elem.id,
                                   name,
                                   pd.Timestamp(elem.timestamp),
                                   len(elem.tags),
                                   tag.k, 
                                   tag.v])


poi_handler = POIHandler(custom_filter={'addr:city':['La Habana']})
poi_handler.apply_file('cuba-latest.osm.pbf')
colnames = ['type', 'id', 'name', 'lon', 'lat','timestamp','n_tags', 'tag_key',
            'tag_value']

df_poi = pd.DataFrame(poi_handler.osm_data, columns=colnames)
df_poi.to_csv('outmap.txt',sep='\t',index=False)
    # Escribir otra cadena de texto en el archivo
print(df_poi.head(4))
