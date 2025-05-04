# 📌 광진구 도로 데이터 + 모래주머니 통합 (위경도 오류 수정 완료)

import pandas as pd
import numpy as np
from shapely.geometry import Point
from scipy.spatial import cKDTree
import geopandas as gpd

# [1] 데이터 불러오기
road_df = pd.read_csv("광진구_염화칼슘통합.csv")
sand_df = pd.read_csv("광진구_모래주머니_위경도.csv")

# [2] NaN 제거 (필요시)
road_df = road_df.dropna(subset=['위도', '경도']).copy()
sand_df = sand_df.dropna(subset=['위도', '경도']).copy()

# [3] GeoDataFrame 변환
road_gdf = gpd.GeoDataFrame(
    road_df,
    geometry=gpd.points_from_xy(road_df['경도'], road_df['위도']),
    crs="EPSG:4326"
)
sand_gdf = gpd.GeoDataFrame(
    sand_df,
    geometry=gpd.points_from_xy(sand_df['경도'], sand_df['위도']),
    crs="EPSG:4326"
)

# [4] 좌표계 변환 (미터단위 계산용)
road_gdf = road_gdf.to_crs(epsg=5186)
sand_gdf = sand_gdf.to_crs(epsg=5186)

# [5] KDTree 구축
sandbag_coords = np.array(list(zip(sand_gdf.geometry.x, sand_gdf.geometry.y)))
road_coords = np.array(list(zip(road_gdf.geometry.x, road_gdf.geometry.y)))

tree = cKDTree(sandbag_coords)

# [6] 거리 매칭 (50m 이내)
dist, idx = tree.query(road_coords, distance_upper_bound=50)

# [7] 매칭 결과 적용
road_gdf['모래주머니여부'] = np.where(dist != np.inf, 1, 0)

# [8] 최종 저장
final_cols = ['도로명', '전체주소', '위도', '경도', '경사도(%)', '열선설치여부','제설함여부','염화칼슘여부', '모래주머니여부']
road_gdf[final_cols].to_csv("광진구_통합_1차.csv", index=False)


