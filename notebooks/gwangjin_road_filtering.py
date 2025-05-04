import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from scipy.spatial import cKDTree
import numpy as np
import matplotlib.pyplot as plt

roads = gpd.read_file("데이터셋/서울시 경사도/등고선 5000/N3L_F001.shp")  # 서울시 도로 선형
elevation = gpd.read_file("데이터셋/서울시 경사도/표고 5000/N3P_F002.shp")  # 서울시 표고점



gwangjin = gpd.read_file("데이터셋/gwangjin_only.geojson")
gwangjin = gwangjin.to_crs(roads.crs)  

def get_start_end(geom):
    coords = list(geom.coords)
    return Point(coords[0]), Point(coords[-1])

roads['start'], roads['end'] = zip(*roads.geometry.apply(get_start_end))
roads['center'] = roads.apply(
    lambda row: Point((row.start.x + row.end.x)/2, (row.start.y + row.end.y)/2), axis=1)

roads_in_gwangjin = roads[roads['center'].apply(lambda p: gwangjin.contains(p).any())]

coords = np.array([[p.x, p.y] for p in elevation.geometry])
heights = elevation['HEIGHT'].values
tree = cKDTree(coords)

start_coords = np.array([[p.x, p.y] for p in roads_in_gwangjin['start']])
end_coords = np.array([[p.x, p.y] for p in roads_in_gwangjin['end']])
_, start_idx = tree.query(start_coords, k=1)
_, end_idx = tree.query(end_coords, k=1)

roads_in_gwangjin = roads_in_gwangjin.copy()

roads_in_gwangjin.loc[:, 'start_height'] = heights[start_idx]
roads_in_gwangjin.loc[:, 'end_height'] = heights[end_idx]
roads_in_gwangjin.loc[:, 'length'] = roads_in_gwangjin.geometry.length
roads_in_gwangjin.loc[:, 'slope_percent'] = (
    (roads_in_gwangjin['end_height'] - roads_in_gwangjin['start_height']) / roads_in_gwangjin['length']) * 100


center_gdf = gpd.GeoDataFrame(
    roads_in_gwangjin[['UFID', 'slope_percent']],
    geometry=roads_in_gwangjin['center'],
    crs=roads.crs
).to_crs(epsg=4326)

center_gdf['latitude'] = center_gdf.geometry.y
center_gdf['longitude'] = center_gdf.geometry.x

center_gdf[['UFID', 'latitude', 'longitude', 'slope_percent']].to_csv("광진구_도로경사도_위경도.csv", index=False)


print("서울 전체 도로 수:", len(roads))
print("광진구 내 필터링된 도로 수:", len(roads_in_gwangjin))

