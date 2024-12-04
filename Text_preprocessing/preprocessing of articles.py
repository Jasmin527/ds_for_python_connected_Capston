import pandas as pd

# 엑셀 파일 경로
file_path = "기사 크롤링.xlsx"  # 입력 파일 경로
output_file = "기사 크롤링_처리결과.xlsx"  # 결과 파일 경로

# # 함수 정의 (직접 입력하는 방식_코드)
# def categorize_result1(value):
#     keywords = [
#         "방역", "소독", "예방", "박멸", "점검",
#         "서울", "종로", "용산", "성동", "광진", "동대문", "중랑", "성북", "강북", "도봉", "노원",
#         "은평", "서대문", "마포", "양천", "강서", "구로", "금천", "영등포", "동작", "관악", "서초",
#         "강남", "송파", "강동", "부산", "부산진", "동래", "해운대", "사하", "금정", "연제",
#         "수영", "사상", "대구", "수성", "달서", "인천", "미추홀", "연수"
#     ]
#     for keyword in keywords:
#         if keyword in str(value):
#             return keyword
#     return ""
#
# def categorize_result2(value):
#     keywords = [
#         "방역", "소독", "예방", "박멸", "점검",
#         "남동", "부평", "계양", "광주", "광산", "대전", "유성", "대덕", "울산", "세종",
#         "경기", "수원", "고양", "용인", "성남", "부천", "안산", "화성", "남양주", "안양",
#         "평택", "의정부", "파주", "시흥", "김포", "광명", "광주", "군포", "이천", "오산",
#         "하남", "양주", "구리", "안성", "포천", "의왕", "여주", "동두천", "과천", "강원",
#         "춘천", "원주", "강릉", "동해", "태백", "속초"
#     ]
#     for keyword in keywords:
#         if keyword in str(value):
#             return keyword
#     return ""
#
# def categorize_result3(value):
#     keywords = [
#         "방역", "소독", "예방", "박멸", "점검",
#         "삼척", "충청북도", "청주", "충주", "제천", "충청남도", "천안", "공주", "보령", "아산",
#         "서산", "논산", "계룡", "당진", "전라북도", "전주", "군산", "익산", "정읍", "남원",
#         "김제", "전라남도", "목포", "여수", "순천", "나주", "광양", "경상북도", "포항", "경주",
#         "김천", "안동", "구미", "영주", "영천", "상주", "문경", "경산", "경상남도", "창원",
#         "진주", "통영", "사천", "김해", "밀양", "거제", "양산", "제주"
#     ]
#     for keyword in keywords:
#         if keyword in str(value):
#             return keyword
#     return ""
#
# # 각 함수를 데이터프레임에 적용하여 결과 저장
# df['result1'] = df[target_column].apply(categorize_result1)
# df['result2'] = df[target_column].apply(categorize_result2)
# df['result3'] = df[target_column].apply(categorize_result3)
#
# # 처리된 데이터 저장
# output_file = "기사 크롤링_처리결과.xlsx"
# df.to_excel(output_file, index=False)
# print(f"결과가 저장되었습니다: {output_file}")

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
def categorize(value, keywords):  # value는 "뉴스제목" 열의 값
    for keyword in keywords:
        # 각 keyword에 대해 value에 해당 키워드가 포함되어 있는지 확인
        if keyword in str(value):
            return keyword
    return ""

# 모든 시트를 하나로 병합
all_sheets = pd.ExcelFile(file_path)
merged_df = pd.DataFrame()

# 파일에 있는 모든 시트 이름 리스트 불러오기
for sheet_name in all_sheets.sheet_names:
    # 각 시트를 데이터 프레임으로 변환
    sheet_df = all_sheets.parse(sheet_name)
    sheet_df['시트명'] = sheet_name  # 각 데이터에 시트명 열 추가
    # 각 시트를 merged_df에 순차적으로 추가
    merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)

# 결과 열 생성
for result_col, keywords in keyword_groups.items():
    # 뉴스 제목이 있는 경우에만 처리
    if '뉴스 제목' in merged_df.columns:
        # 뉴스 제목 열의 각 값(value)에 대해 categorize 함수를 호출
        # 결과를 새로운 열(result1, result2, result3)로 저장
        merged_df[result_col] = merged_df['뉴스 제목'].apply(categorize, keywords=keywords)
    else:
        print(f"'뉴스 제목' 열이 없습니다. 처리할 수 없습니다.")

# 처리된 데이터 저장
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 병합된 데이터 저장
    merged_df.to_excel(writer, index=False, sheet_name='병합된 데이터')

print(f"모든 시트 데이터를 병합하고, 결과를 포함한 파일이 저장되었습니다: {output_file}")