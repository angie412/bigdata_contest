import pandas as pd
import numpy as np
from shapely.geometry import Point
from scipy.spatial import cKDTree
import geopandas as gpd

# [1] 데이터 불러오기
road_df = pd.read_csv("데이터셋/광진구_도로명_위경도_경사도.csv", encoding="utf-8")
heat_df = pd.read_csv("광진구_열선도로_위경도포함.csv", encoding="utf-8")

# [2] 결측치 제거
road_df = road_df.dropna(subset=['위도', '경도']).copy()

# [3] GeoDataFrame 변환
road_gdf = gpd.GeoDataFrame(
    road_df,
    geometry=gpd.points_from_xy(road_df['경도'], road_df['위도']),
    crs="EPSG:4326"
)

heat_start = gpd.GeoDataFrame(
    heat_df,
    geometry=gpd.points_from_xy(heat_df['기점경도'], heat_df['기점위도']),
    crs="EPSG:4326"
)
heat_end = gpd.GeoDataFrame(
    heat_df,
    geometry=gpd.points_from_xy(heat_df['종점경도'], heat_df['종점위도']),
    crs="EPSG:4326"
)

# [4] 좌표계 변환 (거리 계산용)
road_gdf = road_gdf.to_crs(epsg=5186)
heat_start = heat_start.to_crs(epsg=5186)
heat_end = heat_end.to_crs(epsg=5186)

# [5] KDTree 준비
start_coords = np.array(list(zip(heat_start.geometry.x, heat_start.geometry.y)))
end_coords = np.array(list(zip(heat_end.geometry.x, heat_end.geometry.y)))

tree_start = cKDTree(start_coords)
tree_end = cKDTree(end_coords)

road_coords = np.array(list(zip(road_gdf.geometry.x, road_gdf.geometry.y)))

# [6] 거리 매칭 (50m 이내)
dist_start, _ = tree_start.query(road_coords, distance_upper_bound=50)
dist_end, _ = tree_end.query(road_coords, distance_upper_bound=50)

# [7] 열선 설치 여부 판정
road_gdf['열선설치여부'] = np.where(
    (dist_start != np.inf) | (dist_end != np.inf), 1, 0
)

# [8] 최종 저장할 컬럼: 도로명 + 전체주소 + 위도 + 경도 + elevation + 열선설치여부
final_cols = ['도로명', '전체주소', '위도', '경도', '경사도(%)', '열선설치여부']

# [9] 저장
road_gdf[final_cols].to_csv("광진구_도로명_위경도_경사도_열선설치.csv", index=False, encoding="utf-8-sig")



