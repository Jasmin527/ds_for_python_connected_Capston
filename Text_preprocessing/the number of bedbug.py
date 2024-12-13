import pandas as pd

# 엑셀 파일 및 시트 설정
file_path = "기사 크롤링_처리결과.xlsx"  # 기존 파일
output_file = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 저장할 파일 이름

# 엑셀 파일 읽기
df = pd.read_excel(file_path)

# 카운트 대상 열 (result1, result2, result3)
columns_to_count = ['result1', 'result2', 'result3']

# 지역 이름 매핑 (경기 → 경기도, 강원 → 강원도 등)
region_mapping = {
    "서울": "서울특별시",
    "경기": "경기도",
    "강원": "강원도",
    "부산": "부산광역시",
    "대구": "대구광역시",
    "인천": "인천광역시",
    "광주": "광주광역시",
    "대전": "대전광역시",
    "울산": "울산광역시",
    "세종": "세종특별자치시",
    # "충북": "충청북도", # 단어 출력값이 0
    # "충남": "충청남도", # 단어 출력값이 0
    "충청도": "충청도",
    # "전북": "전라북도", # 단어 출력값이 0
    # "전남": "전라남도", # 단어 출력값이 0
    "전라도": "전라도",
    # "경북": "경상북도", # 단어 출력값이 0
    # "경남": "경상남도", # 단어 출력값이 0
    "경상도": "경상도",
    "제주": "제주특별자치도"
}

# 지역별 횟수를 저장할 딕셔너리 초기화
region_counts = {region: 0 for region in region_mapping.values()}

# 매핑된 키워드를 기준으로 각 열에서 카운트
for column in columns_to_count:
    for short_name, full_name in region_mapping.items():
        region_counts[full_name] += df[column].str.contains(short_name, na=False).sum()

# 결과를 데이터프레임으로 변환
summary_df = pd.DataFrame(list(region_counts.items()), columns=['지역', '횟수'])

# 기존 데이터를 새로운 시트에 추가하여 저장
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 원본 데이터 저장
    df.to_excel(writer, index=False, sheet_name='원본 데이터')
    # 요약 결과 저장
    summary_df.to_excel(writer, index=False, sheet_name='지역별 빈도')

print(f"결과가 저장되었습니다: {output_file}")