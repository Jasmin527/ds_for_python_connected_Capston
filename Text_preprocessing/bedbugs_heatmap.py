import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

# 한글 글꼴 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 맑은 고딕 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 엑셀 파일 경로
file_path = "article_crawling_city.xlsx"  # 입력 파일 경로

# 데이터 로드
sheet_name = '지역별 빈도'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 피벗 테이블 생성 (지역별 횟수)
pivot_df = df.pivot_table(index='지역', values='횟수', aggfunc='sum', fill_value=0)

# 히트맵 생성
plt.figure(figsize=(10, 8))
sns.heatmap(pivot_df, cmap='Reds', annot=True, fmt='d', linewidths=.5, cbar_kws={'label': '횟수'})
plt.title('지역별 기사 횟수 히트맵', fontsize=16)
plt.xlabel('지역', fontsize=14)
plt.ylabel('지역', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.tight_layout()

# 히트맵 저장 및 표시
output_image = "지역별_기사_빈도_히트맵.png"
plt.savefig(output_image)
plt.show()
