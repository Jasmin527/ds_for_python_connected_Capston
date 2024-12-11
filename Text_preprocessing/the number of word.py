import pandas as pd

# 엑셀 파일 경로
file_path = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 입력 파일 경로
output_file = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 결과 파일 경로

# 키워드 그룹 정의
keyword_groups = {
    'result': [
        "사우나", "기숙사", "고시원", "가정집", "지하철", "KTX", "무궁화", "원룸", "찜질방", "주택", "중학교", "외국인 숙소",
        "숙박시설", "학교"
    ]
}

# 키워드 검색 함수
def count_keyword_occurrences(value, keywords):
    # 뉴스 제목(value)에서 키워드 목록(keywords)에 포함된 단어의 존재 여부를 확인.
    count = 0
    for keyword in keywords:
        if keyword in str(value):
            count += 1
    return count

# 파일 읽기 및 처리
try:
    # 파일 읽기
    excel_file = pd.ExcelFile(file_path)
    if '기사 크롤링_결과_단어빈도' in excel_file.sheet_names:
        # 이미 시트가 존재하면 로드
        df = pd.read_excel(file_path, sheet_name='기사 크롤링_결과_단어빈도')
    else:
        # 시트가 없으면 병합된 데이터를 사용해 생성
        print("시트가 존재하지 않아 새로 생성합니다.")
        merged_df = pd.DataFrame()
        for sheet_name in excel_file.sheet_names:
            sheet_df = excel_file.parse(sheet_name)
            sheet_df['시트명'] = sheet_name
            merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)
        df = merged_df[['뉴스 제목']] if '뉴스 제목' in merged_df.columns else pd.DataFrame(columns=['뉴스 제목'])

    # 키워드별 뉴스 개수 계산
    if '뉴스 제목' in df.columns:
        keyword_counts = {keyword: 0 for keyword in keyword_groups['result']}  # 키워드 등장 횟수 초기화

        # 각 키워드에 대해 등장 횟수 계산 (regex=False 추가)
        for keyword in keyword_groups['result']:
            keyword_counts[keyword] = df['뉴스 제목'].str.contains(keyword, na=False, regex=False).sum()

        # 결과를 데이터프레임으로 변환
        keyword_count_df = pd.DataFrame(list(keyword_counts.items()), columns=['키워드', '뉴스 개수'])

        # 처리된 데이터 저장
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            keyword_count_df.to_excel(writer, index=False, sheet_name='키워드별 뉴스 개수')

        print(f"'키워드별 뉴스 개수' 시트를 추가하고 결과를 저장했습니다: {output_file}")
    else:
        print("'뉴스 제목' 열이 없습니다. 키워드 분석을 수행할 수 없습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")