import pandas as pd

# [1] 시간대별 사고 데이터 불러오기
time_csv = "데이터셋/서울_시간대별사고데이터.csv"  # ← 네가 경로 수정
df = pd.read_csv(time_csv, encoding='utf-8-sig')

# [2] 사고[건] 데이터만 추출
accident_row = df[(df['사고년도'] == '사고[건]')].reset_index(drop=True)
print(accident_row)
if accident_row.empty:
    raise ValueError("행이 없음")

# [3] 시간대별 사고 건수 가져오기
accident_values = accident_row.iloc[0, 3:].astype(str).str.replace(",", "").astype(float)

# [4] 전체 사고 수 계산
total_accidents = accident_values.sum()

# [5] 시간대 구간별 인덱스 계산
# 컬럼 순서: 00-02 / 02-04 / 04-06 / 06-08 / 08-10 / ... 22-24
# 즉, 0~4 인덱스가 00~10시 (새벽)
# 3~5 인덱스가 6~10시 (출근시간)
# 10,11 인덱스가 20-24시 (야간)

early_morning_indices = list(range(0, 5))  # 00시~10시
commute_peak_indices = [3, 4]              # 06시-08시 + 08시-10시
nighttime_indices = [10, 11]               # 20시-22시 + 22시-24시

# [6] 구간별 사고 수
early_morning_accidents = accident_values.iloc[early_morning_indices].sum()
commute_peak_accidents = accident_values.iloc[commute_peak_indices].sum()
nighttime_accidents = accident_values.iloc[nighttime_indices].sum()

# [7] 비율 계산
early_morning_ratio = early_morning_accidents / total_accidents if total_accidents > 0 else 0
commute_peak_ratio = commute_peak_accidents / total_accidents if total_accidents > 0 else 0
nighttime_ratio = nighttime_accidents / total_accidents if total_accidents > 0 else 0

# [8] 결과 출력
print(f"새벽 사고 비율: {early_morning_ratio:.2%}")
print(f"출근시간 사고 비율: {commute_peak_ratio:.2%}")
print(f"야간 사고 비율: {nighttime_ratio:.2%}")

# [9] 기존 도로 데이터에 병합
road_df = pd.read_csv("광진구_도로_기상_기상노면상태사고_통합.csv")  # ← 네가 경로 수정

road_df["early_morning_accident_ratio"] = early_morning_ratio
road_df["commute_peak_accident_ratio"] = commute_peak_ratio
road_df["nighttime_accident_ratio"] = nighttime_ratio

# [10] 저장
road_df.to_csv("광진구_도로_기상_기상노면상태_시간대사고_통합.csv", index=False, encoding="utf-8-sig")

