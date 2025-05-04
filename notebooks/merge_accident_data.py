# 사고 관련 지표를 도로 데이터에 병합하는 코드

import pandas as pd

# [1] 데이터 로딩
road_df = pd.read_csv("광진구_도로_기상_통합.csv")
weather_accident = pd.read_excel("데이터셋/기상상태별교통사고.xls")
surface_accident = pd.read_excel("데이터셋/노면상태별교통사고.xls")
time_accident = pd.read_excel("데이터셋/시간대별사고데이터.xls")
type_accident = pd.read_excel("데이터셋/사고유형별데이터.xls")

# [2] 사고 데이터 전처리 및 지표 계산

## (1) 겨울철 사고 비율 계산
winter_total = weather_accident['전체건수'].sum()
winter_season = weather_accident.query("기상상태 in ['눈', '서리/결빙']")['전체건수'].sum()
winter_accident_rate = winter_season / winter_total

## (2) 결빙 사고 비율 계산
surface_total = surface_accident['전체건수'].sum()
ice_surface = surface_accident.query("노면상태 == '결빙'")['전체건수'].sum()
icy_surface_accident_rate = ice_surface / surface_total

## (3) 새벽 사고 비율 계산
# 0시 ~ 9시 시간대만
morning_time = time_accident.query("시간대 <= 9")['전체건수'].sum()
time_total = time_accident['전체건수'].sum()
early_morning_accident_rate = morning_time / time_total

## (4) 사고 심각도 점수 계산
# 사망자*3 + 중상자*2 + 경상자*1
fatal = type_accident['사망자수'].sum()
serious = type_accident['중상자수'].sum()
minor = type_accident['경상자수'].sum()
accident_severity_score = (fatal * 3 + serious * 2 + minor * 1) / type_accident['사고건수'].sum()

# [3] 도로 데이터에 지표 추가
road_df['winter_accident_rate'] = winter_accident_rate
road_df['icy_surface_accident_rate'] = icy_surface_accident_rate
road_df['early_morning_accident_rate'] = early_morning_accident_rate
road_df['accident_severity_score'] = accident_severity_score

# [4] 최종 저장
output_path = "./광진구_최종_통합_사고포함.csv"
road_df.to_csv(output_path, index=False, encoding='utf-8-sig')

