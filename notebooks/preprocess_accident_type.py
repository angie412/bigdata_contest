import pandas as pd

# [1] CSV 불러오기 (헤더 없음)
df = pd.read_csv("데이터셋/서울_사고유형별데이터.csv", encoding='utf-8-sig', header=None)

# [2] 각 행 위치 찾기
death_row = df[df.iloc[:, 2] == "사망[명]"].reset_index(drop=True)
injury_row = df[df.iloc[:, 2] == "부상[명]"].reset_index(drop=True)


## [3] 수치 전처리
def parse_values(row):
    return row.iloc[0, 3:].astype(str).str.replace(",", "").replace("-", "0").astype(float)

death_vals = parse_values(death_row)
injury_vals = parse_values(injury_row)

# [4] 결빙 유사 사고 유형 인덱스 (각 연도당 13개 그룹)
ice_type_offsets = [6, 7, 9, 10, 11]  # 추돌, 기타, 도로이탈, 전도전복, 기타
all_indices = []
for base in range(3, 3 + 13 * 4, 13):  # 2020~2023
    all_indices.extend([base + offset for offset in ice_type_offsets])

# [5] 결빙 관련 사망자/부상자 수
ice_deaths = death_vals.iloc[[i - 3 for i in all_indices]].sum()
ice_injuries = injury_vals.iloc[[i - 3 for i in all_indices]].sum()
print(ice_deaths)
print(ice_injuries)
# [6] 심각도 점수 계산
ice_severity_score = int(ice_deaths * 3 + ice_injuries)

# [7] 출력
print("📊 결빙 관련 사고 심각도 분석:")
print(f"- 사망자 수 (결빙 관련): {ice_deaths:.0f}명")
print(f"- 부상자 수 (결빙 관련): {ice_injuries:.0f}명")
print(f"- ☠️ 결빙 심각도 점수: {ice_severity_score:,}")

# [8] 병합 및 저장
road_df = pd.read_csv("광진구_도로_기상_기상노면상태_시간대사고_통합.csv", encoding="utf-8-sig")
road_df["ice_related_severity_score"] = ice_severity_score
road_df.to_csv("광진구_도로_기상_사고_데이터통합.csv", index=False, encoding="utf-8-sig")

