import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 글꼴 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 맑은 고딕 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 엑셀 파일 경로
file_path = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 입력 파일 경로

# '날짜에 따른 지역별 빈도' 시트 데이터 로드
sheet_name = '날짜에 따른 지역별 빈도'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 유효한 열 확인
if all(col in df.columns for col in ['지역', '횟수']):
    # 지역별 횟수 데이터
    regions = df['지역']
    counts = df['횟수']

    # 히스토그램 생성
    plt.figure(figsize=(12, 6))
    plt.bar(regions, counts, color='skyblue')

    # 그래프 꾸미기
    plt.title('지역별 등장 횟수', fontsize=16)
    plt.xlabel('지역', fontsize=14)
    plt.ylabel('횟수', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)  # 지역 이름 회전
    plt.tight_layout()

    # 그래프 저장 및 표시
    output_image = "지역별_등장_횟수_막대그래프.png"
    plt.savefig(output_image)
    plt.show()

    print(f"막대그래프가 생성되고 저장되었습니다: {output_image}")