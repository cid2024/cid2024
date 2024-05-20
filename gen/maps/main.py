import requests
from deep_translator import GoogleTranslator
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

def geocoding(query):
  with requests.get("https://nominatim.openstreetmap.org/search?q="+query+"&format=json&polygon_geojson=1", headers=headers) as response:
    if response.status_code == 200 and response.json() != []:
      return response.json()
    else:
      print("trying query in en...")
      query_en = GoogleTranslator(source='ko', target='en').translate(query)
      print(query_en)
      with requests.get("https://nominatim.openstreetmap.org/search?q="+query_en+"&format=json&polygon_geojson=1", headers=headers) as response:
        if response.status_code == 200:
          if response.json() == []:
            print("Error: Empty response from Nominatim.")
            return None
          else:
            return response.json()
        else:
          print(response.status_code, end=" ")
          print("Error: Cannot fetch response from Nominatim.")
          return None

def display_geojson(geojson):
  if geojson is None:
    print("No result from Nominatim.")
    return
  feature_dict = {"type": "FeatureCollection", "features": [{"id": 0, "type": "Feature", "geometry": geojson[0]['geojson'], "properties": {"col1": "name1"}}]}
  gdf = gpd.GeoDataFrame.from_features(feature_dict)
  gdf = gdf.set_crs("EPSG:4326")
  fig, ax = plt.subplots(figsize=(10, 10))
  gdf.plot(ax=ax, alpha=0.5, edgecolor='k')
  ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.DarkMatterNoLabels)
  plt.savefig('geojson_map.png')
  plt.show()

display_geojson(geocoding("서울시"))