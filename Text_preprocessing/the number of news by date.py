import pandas as pd

# 엑셀 파일 경로
file_path = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 입력 파일 경로
output_file = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 결과 파일 경로

# 데이터 로드
df = pd.read_excel(file_path, sheet_name='원본 데이터')

# 유효한 열 확인
if all(col in df.columns for col in ['날짜', 'result1', 'result2', 'result3']):
    # 날짜별로 지역 리스트 생성 (result1, result2, result3 모두 포함)
    grouped_df = (
        df.groupby('날짜')[['result1', 'result2', 'result3']]
        .apply(
            lambda x: ', '.join(
                x.values.flatten().astype(str)  # 모든 값을 문자열로 변환
            )
        )
        .reset_index(name='같은 날짜 지역')  # 결과를 데이터프레임으로 변환
    )

    # 처리된 데이터 저장
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='new') as writer:
        grouped_df.to_excel(writer, index=False, sheet_name='날짜별 지역 리스트')

    print(f"같은 날짜에 등장한 지역을 추출하여 저장했습니다: {output_file}")
else:
    print("'날짜', 'result1', 'result2', 'result3' 중 하나 이상의 열이 없습니다. 데이터를 확인하세요.")