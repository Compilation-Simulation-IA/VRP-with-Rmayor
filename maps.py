from geopy.geocoders import Nominatim, options
import pandas as pd
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
                     '38 y 5ta A,Vedado,La Habana,Cuba',
                     '23 y M, Vedado, La Habana, Cuba']})

df2[['location_lat', 'location_long']] = df2['Location'].apply(
    geolocator.geocode).apply(lambda x: pd.Series(
        [x.latitude, x.longitude], index=['location_lat', 'location_long']))

latitude = location.latitude
longitude = location.longitude
print(df2.head())
print(latitude, longitude)
