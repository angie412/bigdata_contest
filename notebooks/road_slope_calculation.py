import pandas as pd
import requests
import time
import math
import urllib.parse

# [1] 설정
TXT_PATH = r"C:\Users\82102\OneDrive\바탕 화면\데이터셋\서울_도로명주소_전체.txt"  # 수정해줘
SAVE_PATH = r"C:\Users\82102\OneDrive\바탕 화면\데이터셋\gwangjin_result.csv"  # 수정해줘
API_KEY = ""  # 카카오 REST API 키
HEADERS = {"Authorization": f"KakaoAK {API_KEY}",
           "User-Agent": "Mozilla/5.0"}

# [2] 컬럼명 (24개 반영)
col_names = [
    '도로명주소관리번호', '법정동코드', '시도명', '시군구명', '법정읍면동명', '법정리명',
    '산여부', '지번본번', '지번부번', '도로명코드', '도로명', '지하여부',
    '건물본번', '건물부번', '행정동코드', '행정동명', '기초구역번호', '이전도로명주소',
    '효력발생일', '공동주택구분', '이동사유코드', '건축물대장건물명', '시군구용건물명', '비고'
]

df = pd.read_csv(TXT_PATH, sep='|', encoding='cp949', header=None, names=col_names, usecols=range(24))


# [3] 데이터 불러오기
df = pd.read_csv(TXT_PATH, sep='|', encoding='cp949', header=None, names=col_names, usecols=range(24))
df['시군구명'] = df['시군구명'].astype(str).str.strip()

# [4] 광진구 필터링
gwangjin_df = df[df['시군구명'] == '광진구'].copy()
if gwangjin_df.empty:
    raise ValueError("❗ '광진구' 데이터가 없습니다.")

# [5] 주소 만들기
gwangjin_df['건물번호'] = gwangjin_df.apply(
    lambda row: f"{int(row['건물본번'])}-{int(row['건물부번'])}" if row['건물부번'] != 0 else f"{int(row['건물본번'])}",
    axis=1
)
gwangjin_df['전체주소'] = (
    gwangjin_df['시도명'].astype(str) + " " +
    gwangjin_df['시군구명'].astype(str) + " " +
    gwangjin_df['도로명'].astype(str) + " " +
    gwangjin_df['건물번호'].astype(str)
)

# [6] ufid 생성
gwangjin_df['ufid_num'] = pd.factorize(gwangjin_df['도로명'])[0]
gwangjin_df['ufid'] = gwangjin_df['ufid_num'].apply(lambda x: f"GJ_{x:03d}")

# [7] 위도, 경도 가져오기
def get_coordinates(address):
    try:
        url = "https://dapi.kakao.com/v2/local/search/address.json"
        params = {"query": address}  
        res = requests.get(url, headers=HEADERS, params=params)
        res.raise_for_status()
        docs = res.json().get("documents")
        if docs:
            x = docs[0]["x"]
            y = docs[0]["y"]
            return float(y), float(x)
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"주소 실패: {address} | 에러: {e}")
        return None, None


lat_list = []
lon_list = []

for idx, row in gwangjin_df.iterrows():
    addr = row['전체주소']
    lat, lon = get_coordinates(addr)
    time.sleep(0.3)  # 카카오 정책상 0.3초 대기
    lat_list.append(lat)
    lon_list.append(lon)
    print(f"📍 {addr} → 위도: {lat}, 경도: {lon}")

gwangjin_df['위도'] = lat_list
gwangjin_df['경도'] = lon_list

# [8] 경사도 계산
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # 지구 반지름 (m)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

slope_list = []
grouped = gwangjin_df.groupby('ufid')
for ufid, group in grouped:
    if group.shape[0] < 2:
        avg_slope = None
    else:
        group_valid = group.dropna(subset=['위도', '경도'])
        if group_valid.shape[0] < 2:
            avg_slope = None
        else:
            row_max = group_valid.loc[group_valid['위도'].idxmax()]
            row_min = group_valid.loc[group_valid['위도'].idxmin()]
            elev_diff = row_max['위도'] - row_min['위도']  # 위도 차이를 고도차로 가정
            distance = haversine(row_max['위도'], row_max['경도'], row_min['위도'], row_min['경도'])
            if distance == 0:
                avg_slope = None
            else:
                avg_slope = (elev_diff / distance) * 100
    slope_list.extend([avg_slope] * group.shape[0])

gwangjin_df['경사도(%)'] = slope_list

# [9] 최종 저장
final_df = gwangjin_df[['시도명', '시군구명', '도로명', '전체주소', 'ufid', '위도', '경도', '경사도(%)']]
final_df.to_csv(SAVE_PATH, index=False, encoding='utf-8-sig')

