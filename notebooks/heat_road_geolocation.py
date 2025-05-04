import pandas as pd
import requests
import time

# [1] 설정
API_KEY = ""
HEADERS = {"Authorization": f"KakaoAK {API_KEY}"}

INPUT_CSV = "/Users/hongdaeun/Documents/dev/bigdata_contest/데이터셋/광진구_도로열선_설치현황.csv"
OUTPUT_CSV = "/Users/hongdaeun/Documents/dev/bigdata_contest/광진구_열선도로_위경도포함.csv"

# [2] 함수 - 주소를 위도/경도로 변환
def get_coords(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    params = {"query": address}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            coord = result['documents'][0]['address']
            return coord['y'], coord['x']  # (위도, 경도)
    return None, None

# [3] 데이터 로딩
df = pd.read_csv(INPUT_CSV, encoding='cp949')

# [4] 새로운 컬럼 추가
start_latitudes = []
start_longitudes = []
end_latitudes = []
end_longitudes = []

for idx, row in df.iterrows():
    start_address = row['기점']
    end_address = row['종점']
    
    start_lat, start_lon = get_coords(start_address)
    end_lat, end_lon = get_coords(end_address)
    
    start_latitudes.append(start_lat)
    start_longitudes.append(start_lon)
    end_latitudes.append(end_lat)
    end_longitudes.append(end_lon)
    
    print(f"[{idx+1}/{len(df)}] 기점: ({start_lat}, {start_lon}) / 종점: ({end_lat}, {end_lon})")
    

    time.sleep(0.2)

df['기점위도'] = start_latitudes
df['기점경도'] = start_longitudes
df['종점위도'] = end_latitudes
df['종점경도'] = end_longitudes


df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')

