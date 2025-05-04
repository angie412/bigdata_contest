import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point
from scipy.spatial import cKDTree

# [1] 기존 도로 데이터 읽기
road_df = pd.read_csv("광진구_제설함통합.csv")  # 열선 통합까지 된 파일

# 도로 데이터 NaN 제거
road_df = road_df.dropna(subset=['위도', '경도']).copy()

# 도로 데이터 GeoDataFrame 변환
road_gdf = gpd.GeoDataFrame(
    road_df,
    geometry=gpd.points_from_xy(road_df['경도'], road_df['위도']),
    crs="EPSG:4326"
)

# [2] 염화칼슘 보관함 데이터 읽기
salt_df = pd.read_csv("데이터셋/광진구_염화칼슘보관함_위치.csv",  encoding='utf-8-sig')

# 염화칼슘 위치 GeoDataFrame 변환
salt_gdf = gpd.GeoDataFrame(
    salt_df,
    geometry=gpd.points_from_xy(salt_df['경도'], salt_df['위도']),
    crs="EPSG:4326"
)

# [3] 좌표계 변환 (EPSG:5186, 거리 단위 m)
road_gdf = road_gdf.to_crs(epsg=5186)
salt_gdf = salt_gdf.to_crs(epsg=5186)

# [4] KDTree 생성
salt_coords = np.array(list(zip(salt_gdf.geometry.x, salt_gdf.geometry.y)))
tree_salt = cKDTree(salt_coords)

# 도로 포인트 준비
road_coords = np.array(list(zip(road_gdf.geometry.x, road_gdf.geometry.y)))

# [5] 거리 매칭 (50m 이내)
dist, idx = tree_salt.query(road_coords, distance_upper_bound=50)

# [6] 염화칼슘 보관함 여부 추가
road_gdf['염화칼슘여부'] = np.where(dist != np.inf, 1, 0)

# [7] 최종 저장
final_cols = ['도로명', '전체주소', '위도', '경도', '경사도(%)', '열선설치여부','제설함여부','염화칼슘여부']
road_gdf[final_cols].to_csv("광진구_염화칼슘통합.csv", index=False)


