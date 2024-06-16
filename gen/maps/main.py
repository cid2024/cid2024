import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

from deep_translator import GoogleTranslator
from shapely import Polygon
from shapely.geometry import shape, box

from gen.maps.dictionaries import kor_bbox
from log import get_logger


logger = get_logger(__name__)

plt.rcParams['font.family'] = 'Apple SD Gothic Neo'
plt.rcParams['axes.unicode_minus'] = False

HEADERS = {
    'User-Agent': (
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0.0.0 Safari/537.36"
    ),
}


def kor_ord(idx: int) -> str:
    kor_dict = ['가', '나', '다', '라', '마', '바', '사', '아', '자', '차', '카', '타', '파', '하']
    return '(' + (kor_dict[idx] if idx < len(kor_dict) else chr(ord('A') + idx)) + ')'


def geocoding(query: str):
    with requests.get(
        url=f"https://nominatim.openstreetmap.org/search?q={query}&format=json&polygon_geojson=1",
        headers=HEADERS,
    ) as response:
        if response.status_code == 200 and response.json() != []:
            return response.json()

    logger.debug("trying query in en...")
    query_en = GoogleTranslator(source='ko', target='en').translate(query)
    with requests.get(
        url=f"https://nominatim.openstreetmap.org/search?q={query_en}&format=json&polygon_geojson=1",
        headers=HEADERS,
    ) as response:
        if response.status_code == 200:
            if not response.json():
                logger.error("Error: Empty response from Nominatim.")
                return None

            return response.json()

    logger.error("Error: Cannot fetch response from Nominatim: %d" % response.status_code)
    return None


def gen_bbox(feature_dict: dict) -> Polygon:
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


def display_features(feature_dict: dict, use_points: bool, annotated: bool):
    bbox = gen_bbox(feature_dict)
    gdf_bb = gpd.GeoDataFrame({"name": ["Bounding Box"], "value": [0]}, crs="EPSG:4326", geometry=[bbox])
    gdf_bb = gdf_bb.to_crs(epsg=3857)
    gdf = gpd.GeoDataFrame.from_features(feature_dict, crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)
    fig = plt.figure(figsize=(16, 9))
    ax = plt.subplot()
    gdf.plot(ax=ax, alpha=1, edgecolor='w', color=('black' if use_points else 'lightblue'))
    if annotated:
        gdf['coords'] = gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
        gdf['coords'] = [coords[0] for coords in gdf['coords']]
        for idx, row in gdf.iterrows():
            ax.annotate(
                text=kor_ord(idx),
                xy=row['coords'],
                xytext=(0, (5 if use_points else 0)),
                textcoords='offset points',
                ha='center',
                fontsize='x-large',
                fontweight='heavy',
            )
    gdf_bb.plot(ax=ax, alpha=0)
    assert gdf.crs.to_string() == gdf_bb.crs.to_string()
    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.CartoDB.PositronNoLabels)
    plt.savefig('geojson_map.png')
    plt.show()


def translate_to_points(feature_list: list[dict]) -> list[dict]:
    ret: list[dict] = []
    for feature in feature_list:
        gdf = gpd.GeoDataFrame.from_features({"type": "FeatureCollection", "features": [feature]})
        gdf = gdf.set_crs("EPSG:4326")
        ret.append({
            "id": feature["id"],
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    gdf["geometry"].centroid.x,
                    gdf["geometry"].centroid.y,
                ],
            },
            "properties": {
                "name": feature["properties"]["name"] + "_centroid",
            },
        })

    return ret


def draw_map(query_list: list[str], use_points: bool = False, annotated: bool = False):
    features: list[dict] = []
    n_id = 0
    for query in query_list:
        logger.debug("Sending query: %s" % query)
        geometry = geocoding(query)
        if geometry is None:
            logger.debug("No result from Nominatim.")
            pass
        else:
            logger.debug("Received query")
            if use_points:
                features.append({
                    "id": n_id,
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            geometry[0]['lon'],
                            geometry[0]['lat'],
                        ],
                    },
                    "properties": {
                        "name": query,
                    },
                })
            else:
                features.append({
                    "id": n_id,
                    "type": "Feature",
                    "geometry": geometry[0]['geojson'],
                    "properties": {
                        "name": query,
                    },
                })

            n_id += 1

    if use_points:
        display_features(
            {
                "type": "FeatureCollection",
                "features": translate_to_points(features),
            },
            use_points,
            annotated,
        )
    else:
        display_features(
            {
                "type": "FeatureCollection",
                "features": features,
            },
            use_points,
            annotated,
        )


if __name__ == "__main__":
    draw_map(["북인도양", "인도양"], False, True)
