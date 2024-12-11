import pandas as pd

# 엑셀 파일 경로
file_path = "기사 크롤링.xlsx"  # 입력 파일 경로
output_file = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 결과 파일 경로

# 키워드 사전 정의
keyword_groups = {
    'result1': [
        # 서울 및 수도권 지역 (서울 및 25개의 자치구)
        # 부산, 대구, 인천 등 주요 대도시
        "방역", "소독", "예방", "박멸", "점검",
        "서울", "종로", "용산", "성동", "광진", "동대문", "중랑", "성북", "강북", "도봉", "노원",
        "은평", "서대문", "마포", "양천", "강서", "구로", "금천", "영등포", "동작", "관악", "서초",
        "강남", "송파", "강동", "부산", "부산진", "동래", "해운대", "사하", "금정", "연제",
        "수영", "사상", "대구", "수성", "달서", "인천", "미추홀", "연수"
    ],
    'result2': [
        # 경기 및 강원도 주요 도시 포함
        # 광주, 대전, 울산, 세종 등 특별시 및 광역시
        "방역", "소독", "예방", "박멸", "점검",
        "남동", "부평", "계양", "광주", "광산", "대전", "유성", "대덕", "울산", "세종",
        "경기", "수원", "고양", "용인", "성남", "부천", "안산", "화성", "남양주", "안양",
        "평택", "의정부", "파주", "시흥", "김포", "광명", "광주", "군포", "이천", "오산",
        "하남", "양주", "구리", "안성", "포천", "의왕", "여주", "동두천", "과천", "강원",
        "춘천", "원주", "강릉", "동해", "태백", "속초"
    ],
    'result3': [
        # 충청도, 전라도, 경상도, 제주도 등 도 단위 행정구역
        # 전주, 여수, 포항, 창원 등 각 도의 중심 도시 포함
        "방역", "소독", "예방", "박멸", "점검",
        "삼척", "충청북도", "청주", "충주", "제천", "충청남도", "천안", "공주", "보령", "아산",
        "서산", "논산", "계룡", "당진", "전라북도", "전주", "군산", "익산", "정읍", "남원",
        "김제", "전라남도", "목포", "여수", "순천", "나주", "광양", "경상북도", "포항", "경주",
        "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산", "경상남도", "창원",
        "진주", "통영", "사천", "김해", "밀양", "거제", "양산", "제주"
    ]
}

# 키워드 검색 함수
def categorize(value, keywords):
    for keyword in keywords:
        if keyword in str(value):
            return keyword
    return ""

# 모든 시트를 하나로 병합
all_sheets = pd.ExcelFile(file_path)
merged_df = pd.DataFrame()

for sheet_name in all_sheets.sheet_names:
    sheet_df = all_sheets.parse(sheet_name)
    sheet_df['시트명'] = sheet_name
    merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)

# 지역 결과 열 생성
for result_col, keywords in keyword_groups.items():
    if '뉴스 제목' in merged_df.columns:
        merged_df[result_col] = merged_df['뉴스 제목'].apply(categorize, keywords=keywords)

# 중복된 뉴스 제거 및 그룹화
if '날짜' in merged_df.columns:
    # 중복된 뉴스 제목 제거 (날짜와 지역 기준)
    unique_news_df = merged_df.drop_duplicates(subset=['날짜', '뉴스 제목'])

    # 날짜별 뉴스 개수 계산
    grouped_df = unique_news_df.groupby('날짜', as_index=False).agg({
        '뉴스 제목': 'count'
    }).rename(columns={'뉴스 제목': '뉴스 개수'})

    # 처리된 데이터 저장
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        merged_df.to_excel(writer, index=False, sheet_name='병합된 데이터')
        grouped_df.to_excel(writer, index=False, sheet_name='날짜별 뉴스 개수')

    print(f"날짜별 뉴스 개수를 계산하고 저장했습니다: {output_file}")
else:
    print("'날짜' 열이 없습니다. 날짜별 그룹화를 수행할 수 없습니다.")