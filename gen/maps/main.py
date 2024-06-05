import requests
from deep_translator import GoogleTranslator
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from shapely.geometry import shape, box
from .dictionaries import kor_bbox

plt.rcParams['font.family'] ='Apple SD Gothic Neo'
plt.rcParams['axes.unicode_minus'] =False

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

def korord(ord):
  dict = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']
  if ord < len(dict): return '('+dict[ord]+')'
  else: return '('+chr(ord('A')+ord)+')'

def geocoding(query):
  with requests.get("https://nominatim.openstreetmap.org/search?q="+query+"&format=json&polygon_geojson=1", headers=HEADERS) as response:
    if response.status_code == 200 and response.json() != []:
      return response.json()
    else:
      print("trying query in en...")
      query_en = GoogleTranslator(source='ko', target='en').translate(query)
      print(query_en)
      with requests.get("https://nominatim.openstreetmap.org/search?q="+query_en+"&format=json&polygon_geojson=1", headers=HEADERS) as response:
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
  return box(minx=-180, miny=-60, maxx=180, maxy=75)

def display_features(feature_dict, points, annotated):
  bbox = gen_bbox(feature_dict)
  gdf_bb = gpd.GeoDataFrame({"name": ["Bounding Box"], "value": [0]}, crs="EPSG:4326", geometry=[bbox])
  gdf_bb = gdf_bb.to_crs(epsg=3857)
  gdf = gpd.GeoDataFrame.from_features(feature_dict, crs="EPSG:4326")
  gdf = gdf.to_crs(epsg=3857)
  fig = plt.figure(figsize=(16, 9))
  ax = plt.subplot()
  gdf.plot(ax=ax, alpha=1, edgecolor='w', color=('black' if points else 'lightblue'))
  if annotated:
    gdf['coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    gdf['coords'] = [coords[0] for coords in gdf['coords']]
    for idx, row in gdf.iterrows():
      ax.annotate(text=korord(idx), xy=row['coords'], xytext=(0, (5 if points else 0)), textcoords='offset points', ha='center', fontsize='x-large', fontweight='heavy')
  gdf_bb.plot(ax=ax, alpha=0)
  assert gdf.crs.to_string() == gdf_bb.crs.to_string()
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

def draw_map(query_list, points=False, annotated=False):
  features = []
  id = 0
  for query in query_list:
    print("Sending query: " + query)
    geometry = geocoding(query)
    if geometry is None:
      print(f"Error in query {query}: No result from Nominatim.")
    else:
      print("Received query: " + query)
      if points:
        features.append({"id": id, "type": "Feature", "geometry": {"type": "Point", "coordinates": [geometry[0]['lon'], geometry[0]['lat']]}, "properties": {"name": query}})
      else:
        features.append({"id": id, "type": "Feature", "geometry": geometry[0]['geojson'], "properties": {"name": query}})
      id += 1
  if points:
    display_features({"type": "FeatureCollection", "features": translate_to_points(features)}, points, annotated)
  else:
    display_features({"type": "FeatureCollection", "features": features}, points, annotated)

draw_map(["북인도양","인도양"], False, True)