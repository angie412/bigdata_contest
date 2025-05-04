import pandas as pd

# [1] 노면 상태별 교통사고 데이터 불러오기
ice_csv = "데이터셋/서울_노면상태별교통사고.csv"
df = pd.read_csv(ice_csv, encoding='utf-8-sig', header=[0, 1])

# [2] '사고[건]'에 해당하는 행 추출
accident_row = df[df.iloc[:, 1] == "사고[건]"].reset_index(drop=True)

print("__________")
print(accident_row)
# [3] 수치 데이터 전처리 (쉼표 제거 → 정수 변환)
accident_values = accident_row.iloc[0, 2:].astype(str).str.replace(",", "").astype(float)
print(accident_values)

# [4] 컬럼 이름에서 결빙 관련 키워드가 포함된 열 찾기
ice_keywords = ["서리", "결빙", "적설", "해빙"]
ice_columns = [col for col in accident_values.index if any(keyword in col[1] for keyword in ice_keywords)]

print("__________")
print(ice_columns)
# [5] 전체 사고 수 & 결빙 사고 수 & 비율 계산
total_accidents = accident_values.sum()
ice_accidents = accident_values[ice_columns].sum()
ice_ratio = round(ice_accidents / total_accidents, 4) if total_accidents > 0 else 0

# [6] 결과 출력
print(" 노면 상태 기반 사고 통계:")
print(f"전체 사고 건수: {total_accidents:,}건")
print(f"결빙 관련 사고: {ice_accidents:,}건")
print(f"결빙 사고 비율: {ice_ratio:.2%}")

# [7] 도로 데이터와 병합
road_df = pd.read_csv("광진구_도로_기상_기상상태사고_통합.csv")
road_df["icy_surface_accident_ratio"] = ice_ratio

# [8] 저장
road_df.to_csv("광진구_도로_기상_기상노면상태사고_통합.csv", index=False, encoding="utf-8-sig")
