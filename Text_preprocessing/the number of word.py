import pandas as pd

# 엑셀 파일 경로
file_path = "기사 크롤링_처리결과.xlsx"  # 입력 파일 경로
output_file = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 결과 파일 경로

# 키워드 그룹 정의
keyword_groups = {
    'result': [
        "인천 서구 사우나", "대구 계명대 기숙사", "대구 부천 고시원", "서울 고시원", "서울 가정집", "서울 빈대 확인 18곳", "인천 1평 방",
        "서울 빈대 발견 신고 17건", "서울 지하철, KTX", "수원역 무궁화->대전KTX->(동)대구", "서울 빈대 출몰 23건", "충남 아산 원룸",
        "서울 강남구 대형 찜질방", "충남 서산", "기숙학원 빈대", "충남 당진 주택", "경기 인천 중학교", "경기도 수원 일반 주택",
        "경기 빈대 확인 5건", "충남 천안 대학 기숙사", "대전 서구 가정집 2곳", "충북 충주 가정집(다세대주택)", "부산 사하구 가정집",
        "전남 진도군 의신면 김양식장 외국인 숙소", "울산 울주군 원룸", "광주 서구 쌍촌동 단독주택 반지하", "충북 청주 가정집 2곳",
        "충북 진천 숙박시설 1곳", "대구 고교 기숙사", "인천 서구 중학교(재발)", "강원 원주 외국인 기숙사", "목포 찜질방",
        "충청북도 진천시 가정집", "충청북도 청주 가정집", "충청북도 음성 가정집", "충청남도 보령 동대동"
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
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='기사 크롤링_결과_단어빈도')
            keyword_count_df.to_excel(writer, index=False, sheet_name='키워드별 뉴스 개수')

        print(f"'기사 크롤링_결과_단어빈도' 시트를 처리하고 결과를 저장했습니다: {output_file}")
    else:
        print("'뉴스 제목' 열이 없습니다. 키워드 분석을 수행할 수 없습니다.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
