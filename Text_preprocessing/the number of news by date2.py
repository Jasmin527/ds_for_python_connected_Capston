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

# 지역별 횟수를 저장할 딕셔너리 초기화
region_counts = {region: 0 for region in region_mapping.values()}

# 각 날짜별로 지역을 세기 위해, '날짜' 컬럼이 있다고 가정합니다.
# 각 날짜별로 지역이 포함되었으면 해당 지역을 한 번만 카운트하도록 처리

for column in columns_to_count:
    for short_names, full_name in region_mapping.items():
        # 날짜별로 해당 지역이 포함되었는지 확인하고, 중복을 피하기 위해 'drop_duplicates' 사용
        for date in df['날짜'].drop_duplicates():  # '날짜' 컬럼에서 중복을 제거하고 순차적으로 확인
            # 해당 날짜에 해당 지역이 포함되어 있으면 카운트
            for short_name in short_names:  # short_names는 튜플이므로 각 항목에 대해 확인
                # str.contains()에서 regex=False로 지정하여 정규식 오류를 피함
                region_in_date = df[df['날짜'] == date][column].str.contains(short_name, na=False, regex=False)
                if region_in_date.any():  # 해당 날짜에 지역이 포함된 경우
                    region_counts[full_name] += 1  # 날짜당 한번만 카운트

# 결과를 데이터프레임으로 변환
summary_df = pd.DataFrame(list(region_counts.items()), columns=['지역', '횟수'])

# 기존 데이터를 새로운 시트에 추가하여 저장
with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    # 기존 시트를 덮어쓰고 새로운 데이터 작성
    df.to_excel(writer, index=False, sheet_name='원본 데이터')
    summary_df.to_excel(writer, index=False, sheet_name='날짜에 따른 지역별 빈도')

print(f"결과가 저장되었습니다: {output_file}")