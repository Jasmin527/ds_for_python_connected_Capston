import pandas as pd

# 파일 경로 설정
file_path = "기사 크롤링_처리결과.xlsx"  # 기존 파일
output_file = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 저장할 파일 이름

# 키워드 그룹 정의
keyword_groups = {
    'result': [
        "사우나", "기숙사", "고시원", "가정집", "지하철", "KTX", "무궁화", "원룸", "찜질방", "주택", "중학교", "외국인 숙소",
        "숙박시설", "학교"
    ]
}

# 지역 이름 매핑 (예: 경기 → 경기도, 강원 → 강원도 등)
region_mapping = {
    ("서울", "종로", "용산", "성동", "광진", "동대문", "중랑", "성북", "강북", "도봉", "노원", "은평", "서대문", "마포", "양천",
     "강서", "구로", "금천", "영등포", "동작", "관악", "서초", "강남", "송파", "강동"): "서울특별시",
    ("경기", "수원", "고양", "용인", "성남", "부천", "안산", "화성", "남양주", "안양", "평택", "의정부", "파주", "시흥", "김포",
     "광명", "광주", "군포", "이천", "오산", "하남", "양주", "구리", "안성", "포천", "의왕", "여주", "동두천", "과천"): "경기도",
    ("강원", "춘천", "원주", "강릉", "동해", "태백", "속초", "삼척"): "강원도",
    ("부산", "부산진", "동래", "해운대", "사하", "금정", "연제", "수영", "사상"): "부산광역시",
    ("대구", "수성", "달서"): "대구광역시",
    ("인천", "미추홀", "연수", "남동", "부평", "계양"): "인천광역시",
    ("광주", "광산"): "광주광역시",
    ("대전", "유성", "대덕"): "대전광역시",
    "울산": "울산광역시",
    "세종": "세종특별자치시",
    ("충청북도", "청주", "충주", "제천", "충청남도", "천안", "공주", "보령", "아산", "서산", "논산", "계룡", "당진"): "충청도",
    ("전라북도", "전주", "군산", "익산", "정읍", "남원", "김제", "전라남도", "목포", "여수", "순천", "나주", "광양"): "전라도",
    ("경상북도", "포항", "경주", "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산", "경상남도", "창원", "진주", "통영",
     "사천", "김해", "밀양", "거제", "양산"): "경상도",
    "제주": "제주특별자치도"
}

# 데이터 로드
df = pd.read_excel(file_path)

# 카운트 대상 열 (result1, result2, result3)
columns_to_count = ['result1', 'result2', 'result3']

# 지역별 빈도 계산
region_counts = {region: 0 for region in region_mapping.values()}
for column in columns_to_count:
    for short_names, full_name in region_mapping.items():
        for short_name in short_names:
            region_counts[full_name] += df[column].str.contains(short_name, na=False).sum()

# 지역별 빈도 결과 데이터프레임으로 변환
region_summary_df = pd.DataFrame(list(region_counts.items()), columns=['지역', '횟수'])

# 날짜별 지역 빈도 계산
date_region_counts = []
for date in df['날짜'].drop_duplicates():
    date_df = df[df['날짜'] == date]
    for column in columns_to_count:
        for short_names, full_name in region_mapping.items():
            for short_name in short_names:
                # 중복 제외 후 지역 카운트
                region_in_date = date_df[column].str.contains(short_name, na=False, regex=False)
                if region_in_date.any():
                    if not any(item['지역'] == full_name and item['날짜'] == date for item in date_region_counts):
                        date_region_counts.append({'날짜': date, '지역': full_name, '횟수': 1})

# 날짜별 지역 빈도 데이터프레임 변환
date_region_df = pd.DataFrame(date_region_counts).groupby(['지역'], as_index=False)['횟수'].sum()

# 지역 순서 정렬
region_order = list(region_mapping.values())  # 지역 맵핑 순서 리스트
date_region_df['지역'] = pd.Categorical(date_region_df['지역'], categories=region_order, ordered=True)
date_region_df = date_region_df.sort_values(by='지역')  # 지역 순서에 따라 정렬

# 키워드별 뉴스 개수 계산
keyword_counts = {keyword: 0 for keyword in keyword_groups['result']}
for keyword in keyword_groups['result']:
    keyword_counts[keyword] = df['뉴스 제목'].str.contains(keyword, na=False, regex=False).sum()

# 키워드별 뉴스 개수 데이터프레임 변환
keyword_summary_df = pd.DataFrame(list(keyword_counts.items()), columns=['키워드', '뉴스 개수'])

# 결과 저장
with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
    # 원본 데이터 저장
    df.to_excel(writer, index=False, sheet_name='원본 데이터')
    # 지역별 빈도 저장
    region_summary_df.to_excel(writer, index=False, sheet_name='지역별 빈도')
    # 날짜별 지역 빈도 저장
    date_region_df.to_excel(writer, index=False, sheet_name='날짜별 지역 빈도')
    # 키워드별 뉴스 개수 저장
    keyword_summary_df.to_excel(writer, index=False, sheet_name='키워드별 뉴스 개수')

print(f"결과가 저장되었습니다: {output_file}")