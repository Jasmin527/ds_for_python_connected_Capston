import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns

# 한글 글꼴 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 맑은 고딕 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 엑셀 파일 경로
file_path = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 입력 파일 경로

# '키워드별 빈도' 시트 데이터 로드
sheet_name = '키워드별 뉴스 개수'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 색상을 뉴스 개수에 따라 조정
norm = plt.Normalize(df['뉴스 개수'].min(), df['뉴스 개수'].max())
colors = plt.cm.Blues(norm(df['뉴스 개수']))

# 히스토그램 생성
plt.figure(figsize=(12, 6))
bars = plt.bar(df['키워드'], df['뉴스 개수'], color=colors, edgecolor='black')

# 그래프 꾸미기
plt.title('키워드별 기사 개수 히스토그램', fontsize=16)
plt.xlabel('키워드', fontsize=14)
plt.ylabel('뉴스 개수', fontsize=14)

# x축에 키워드 이름 표시
plt.xticks(ticks=df['키워드'], labels=df['키워드'], rotation=45, ha='right', fontsize=10)

# 컬러바 추가
sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical')
cbar.set_label('뉴스 개수', fontsize=12)

plt.tight_layout()

# 그래프 저장 및 표시
output_image = "키워드별_개수_빈도_히스토그램.png"
plt.savefig(output_image)
plt.show()