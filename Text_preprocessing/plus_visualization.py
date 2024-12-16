import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

# 한글 글꼴 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 맑은 고딕 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 엑셀 파일 경로
file_path = "기사 크롤링_처리결과_도시별빈도.xlsx"  # 입력 파일 경로

# 대시보드 생성
fig, axes = plt.subplots(3, 1, figsize=(15, 20))  # 3개의 시각화를 세로로 배치
fig.subplots_adjust(hspace=0.5)  # 그래프 사이에 간격 추가

# 1. 히트맵 생성 (지역별 빈도)
df_heatmap = pd.read_excel(file_path, sheet_name='지역별 빈도')
pivot_df = df_heatmap.pivot_table(index='지역', values='횟수', aggfunc='sum', fill_value=0)
sns.heatmap(pivot_df, cmap='Reds', annot=True, fmt='d', linewidths=.5, cbar_kws={'label': '횟수'}, ax=axes[0])
axes[0].set_title('지역별 기사 횟수 히트맵', fontsize=16)
axes[0].set_xlabel('지역', fontsize=14)
axes[0].set_ylabel('지역', fontsize=14)

# 2. 막대그래프 생성 (날짜별 지역 빈도)
df_bar = pd.read_excel(file_path, sheet_name='날짜별 지역 빈도')
regions = df_bar['지역']
counts = df_bar['횟수']
axes[1].bar(regions, counts, color='skyblue', edgecolor='black')
axes[1].set_title('지역별 등장 횟수', fontsize=16)
axes[1].set_xlabel('지역', fontsize=14)
axes[1].set_ylabel('횟수', fontsize=14)
axes[1].tick_params(axis='x', rotation=45)

# 3. 히스토그램 생성 (키워드별 뉴스 개수)
df_histogram = pd.read_excel(file_path, sheet_name='키워드별 뉴스 개수')
norm = plt.Normalize(df_histogram['뉴스 개수'].min(), df_histogram['뉴스 개수'].max())
colors = plt.cm.Blues(norm(df_histogram['뉴스 개수']))
bars = axes[2].bar(df_histogram['키워드'], df_histogram['뉴스 개수'], color=colors, edgecolor='black')
axes[2].set_title('키워드별 기사 개수 히스토그램', fontsize=16)
axes[2].set_xlabel('키워드', fontsize=14)
axes[2].set_ylabel('뉴스 개수', fontsize=14)
axes[2].tick_params(axis='x', rotation=45)

# 컬러바 추가
sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=axes[2], orientation='vertical', pad=0.02)
cbar.set_label('뉴스 개수', fontsize=12)

# 대시보드 저장 및 표시
output_image = "대시보드_지역_키워드_히트맵.png"
plt.savefig(output_image)
plt.show()