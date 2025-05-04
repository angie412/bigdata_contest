import pandas as pd
import requests
import time

# [1] 설정
KAKAO_API_KEY = "c8a14fd9426b1babed75b56cc3634f56"  # 꼭 본인 키로 바꿔야 해!
KAKAO_HEADERS = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

INPUT_CSV = "데이터셋/광진구_모래주머니 배치현황.csv"
OUTPUT_CSV = "데이터셋/광진구_모래주머니_위경도.csv"

# [2] 데이터 불러오기
df = pd.read_csv(INPUT_CSV,encoding='cp949' )

# [3] 주소 컬럼 정리 (필요 시 수정)
# 예시로 '위치'라는 컬럼에 주소가 있다고 가정
addresses = df["위치"].tolist()

# [4] 위도 경도 추출 함수
def get_lat_lon(address):
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        params = {"query": address}
        res = requests.get(url, headers=KAKAO_HEADERS, params=params)
        if res.status_code == 200:
            result = res.json()
            if result['documents']:
                lon = float(result['documents'][0]['x'])
                lat = float(result['documents'][0]['y'])
                return lat, lon
    except Exception as e:
        print(f"Error for {address}: {e}")
    return None, None

# [5] 주소 → 위경도 변환
latitudes = []
longitudes = []

for addr in addresses:
    lat, lon = get_lat_lon(addr)
    latitudes.append(lat)
    longitudes.append(lon)
    time.sleep(0.3)  # 카카오 API rate limit (0.3초 정도 쉬어주기)

# [6] 결과 저장
df["위도"] = latitudes
df["경도"] = longitudes

df.to_csv(OUTPUT_CSV, index=False)

