import pandas as pd

# 파일 경로 정의
file1_path = "2023_bedbug_check"  # 첫 번째 CSV 파일
file2_path = "2023_bedbug_declaration.csv"  # 두 번째 CSV 파일
output_file = "2023_bedbug_integration.csv"  # 통합된 CSV 파일 경로
processed_file = "article_crawling.xlsx"  # 처리된 결과 저장 경로

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

# 키워드 검색 함수 정의
def categorize(value, keywords):
    """지정된 키워드 목록을 기준으로 값(value)을 검색."""
    for keyword in keywords:
        if keyword in str(value):
            return keyword
    return ""

# 1. 두 CSV 파일 병합
df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# 두 데이터를 병합하고 중복 제거 (중복 기준은 모든 열이 동일한 경우)
merged_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates()

# 병합된 데이터를 CSV 파일로 저장
merged_df.to_csv(output_file, index=False)
print(f"병합된 데이터가 '{output_file}'로 저장되었습니다.")

# 2. 키워드 분석
# 결과 열 생성
for result_col, keywords in keyword_groups.items():
    if '뉴스 제목' in merged_df.columns:
        merged_df[result_col] = merged_df['뉴스 제목'].apply(categorize, keywords=keywords)
    else:
        print(f"'뉴스 제목' 열이 없습니다. 처리할 수 없습니다.")

# 3. 처리된 데이터를 엑셀 파일로 저장
with pd.ExcelWriter(processed_file, engine='openpyxl') as writer:
    merged_df.to_excel(writer, index=False, sheet_name='통합 데이터')

print(f"처리된 데이터가 '{processed_file}'로 저장되었습니다.")
