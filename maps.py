from geopy.geocoders import Nominatim, options
import pandas as pd
import math
import queue
#from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
                       )

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