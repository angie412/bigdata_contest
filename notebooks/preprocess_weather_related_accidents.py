import pandas as pd

# [1] CSV 로드
csv_path = "데이터셋/서울_기상상태별교통사고.csv"
df = pd.read_csv(csv_path, encoding='utf-8-sig')

# [2] 필요 행 필터링
accident_row = df[(df.iloc[:, 0] == "서울") & (df.iloc[:, 1] == "사고[건]")].reset_index(drop=True)
death_row    = df[(df.iloc[:, 0] == "서울") & (df.iloc[:, 1] == "사망[명]")].reset_index(drop=True)
injury_row   = df[(df.iloc[:, 0] == "서울") & (df.iloc[:, 1] == "부상[명]")].reset_index(drop=True)

# [3] 숫자 변환 함수 정의
def extract_numeric_row(row):
    return row.iloc[0, 2:].astype(str).str.replace(",", "").astype(float)

try:
    # [4] 총합 및 눈 상태 사고 계산
    accident_values = extract_numeric_row(accident_row)
    snow_indices = list(range(8, len(accident_values), 7))  # 매 7번째가 '눈' 조건
    snow_accidents = accident_values.iloc[snow_indices].sum()
    total_accidents = accident_values.sum()
    snow_ratio = snow_accidents / total_accidents if total_accidents > 0 else 0

    # [5] 사고 심각도 계산
    total_deaths = extract_numeric_row(death_row).sum()
    total_injuries = extract_numeric_row(injury_row).sum()
    seriousness_score = 2 * total_deaths + total_injuries

    # [6] 출력
    print("📊 서울시 사고 통계 기반 지표:")
    print(f"- ❄️ 눈 상태 사고 비율: {snow_ratio:.2%}")
    print(f"- 🧊 겨울철 사고 건수 (전체 사고수로 대체): {total_accidents:,.0f}건")
    print(f"- ☠️ 사고 심각도 점수: {seriousness_score:,.0f}")

except Exception as e:
    print("🚨 오류 발생:", e)


road_df = pd.read_csv("광진구_도로_기상_통합.csv")

# [2] 새 컬럼 추가
road_df["snow_accident_ratio"] = snow_ratio
road_df["winter_accident_count"] = total_accidents
road_df["seriousness_score"] = seriousness_score

# [3] 저장
road_df.to_csv("광진구_도로_기상_기상상태사고_통합.csv", index=False, encoding="utf-8-sig")

