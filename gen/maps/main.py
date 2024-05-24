import requests
from deep_translator import GoogleTranslator
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import shape, box
from .dictionaries import kor_bbox

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
        
def gen_bbox(feature_dict):
  for bbox in kor_bbox:
    bbox_shape = box(minx=bbox[1], miny=bbox[0], maxx=bbox[3], maxy=bbox[2])
    flag = True
    for feature in feature_dict["features"]:
      geometry = shape(feature["geometry"])
      if not geometry.within(bbox_shape):
        flag = False
        break
    if flag:
      return bbox_shape
  return box(minx=-175, miny=-80, maxx=175, maxy=80)

def display_features(feature_dict):
  bbox = gen_bbox(feature_dict)
  bbox_x, bbox_y = bbox.exterior.xy
  gdf = gpd.GeoDataFrame.from_features(feature_dict)
  gdf = gdf.set_crs("EPSG:4326")
  fig, ax = plt.subplots(figsize=(10, 10))
  gdf.plot(ax=ax, alpha=1, edgecolor='w')
  ax.fill(bbox_x, bbox_y, alpha=0)
  ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.PositronNoLabels)
  plt.savefig('geojson_map.png')
  plt.show()

def translate_to_points(feature_list):
  ret = []
  for feature in feature_list:
    gdf = gpd.GeoDataFrame.from_features({"type": "FeatureCollection", "features": [feature]})
    gdf = gdf.set_crs("EPSG:4326")
    ret.append({"id": feature["id"], "type": "Feature", "geometry": {"type": "Point", "coordinates": [gdf["geometry"].centroid.x, gdf["geometry"].centroid.y]}, "properties": {"name": feature["properties"]["name"] + "_centroid"}})
  return ret

def draw_map(query_list, points=False):
  features = []
  id = 0
  for query in query_list:
    print("Sending query: " + query)
    geometry = geocoding(query)
    if geometry is None:
      print(f"Error in query {query}: No result from Nominatim.")
    else:
      print("Received query: " + query)
      features.append({"id": id, "type": "Feature", "geometry": geometry[0]['geojson'], "properties": {"name": query}})
      id += 1
  if points:
    display_features({"type": "FeatureCollection", "features": translate_to_points(features)})
  else:
    display_features({"type": "FeatureCollection", "features": features})

draw_map(["요르단", "쿠웨이트", "바레인", "오만"], True)