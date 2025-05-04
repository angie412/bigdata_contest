import pandas as pd

# [1] 통합 파일 불러오기 (네가 가지고 있는 파일 경로로 수정해줘)
road_df = pd.read_csv("광진구_도로명_위경도_경사도_열선설치.csv")

# [2] 열선 설치 여부가 1인 도로만 필터링
heating_installed = road_df[road_df['열선설치여부'] == 1].copy()

# [3] 필요한 열만 출력
print(heating_installed[['도로명', '전체주소', '위도', '경도', '경사도(%)', '열선설치여부']])

