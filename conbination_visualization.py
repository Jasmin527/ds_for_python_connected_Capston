import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import rcParams
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib import font_manager, rc
import folium

# 1. 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 맑은 고딕 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)
rcParams['axes.unicode_minus'] = False  # 마이너스 기호도 제대로 표시되도록 설정

# 2. 엑셀 파일 경로 설정 및 읽기
excel_file = "article_crawling_city.xlsx"
file_paths = [
    "2023_09_bedbug.csv",
    "2023_10_bedbug.csv",
    "2023_11_bedbug.csv",
   ]

file_paths2 = [
    "2024_09_bedbug.csv",
    "2024_10_bedbug.csv",
    "2024_11_bedbug.csv"
]

# 3. 대화형 지도 생성 및 저장
locations = {
    "서울특별시": [37.5729, 126.9794],
    "경기도": [37.2636, 127.0286],
    "강원도": [37.8816, 127.7291],
    "부산광역시": [35.1068, 129.0312],
    "대구광역시": [35.8683, 128.5988],
    "인천광역시": [37.4643, 126.5904],
    "광주광역시": [35.1399, 126.9194],
    "대전광역시": [36.3515, 127.4239],
    "울산광역시": [35.5664, 129.3190],
    "세종특별자치시": [36.4801, 127.2889],
    "충청도": [36.6419, 127.4898],
    "전라도": [35.8242, 127.1489],
    "경상도": [35.8722, 128.6025],
    "제주특별자치도": [33.4996, 126.5312]
}

def get_color(value):
    if value <= 10:
        return "green"
    elif 11 <= value <= 20:
        return "yellow"
    elif 21 <= value <= 30:
        return "orange"
    else:
        return "red"

# Folium을 활용한 대화형 지도 생성
df_bar = pd.read_excel(excel_file, sheet_name=2)
folium_map = folium.Map(location=[36.5, 127.5], zoom_start=7)

for _, row in df_bar.iterrows():
    region = row['지역']
    count = row['횟수']
    if region in locations:
        lat, lon = locations[region]
        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            color=get_color(count),
            fill=True,
            fill_color=get_color(count),
            fill_opacity=0.7,
            tooltip=f"{region}: {count}회"
        ).add_to(folium_map)

# 대화형 지도 저장
folium_map.save("23.10.13-11.30 한국 빈대 출몰 현황.html")

# 4. 히트맵 생성 (지역별 빈도)
df_heatmap = pd.read_excel(excel_file, sheet_name=1)
pivot_df = df_heatmap.pivot_table(index='지역', values='횟수', aggfunc='sum', fill_value=0)
plt.figure(figsize=(8, 6))
sns.heatmap(pivot_df, cmap='Reds', annot=True, fmt='d', linewidths=.5, cbar_kws={'label': '횟수'})
plt.title('지역별 빈대 확인/신고 기사 집중도', fontsize=16)
plt.xlabel('지역', fontsize=10)
plt.ylabel('지역', fontsize=10)
plt.savefig("지역별_빈대_확인_신고_기사_집중도.png")
plt.show()

# 5. 막대그래프 생성 (날짜에 따른 지역별 빈도)
regions = df_bar['지역']
counts = df_bar['횟수']
plt.figure(figsize=(12, 6))
plt.bar(regions, counts, color='skyblue', edgecolor='black')
plt.title('날짜에 따른 지역별 빈대 출몰 기사 수', fontsize=16)
plt.xlabel('지역', fontsize=10)
plt.ylabel('횟수', fontsize=10)
plt.xticks(rotation=45)
plt.savefig("날짜에_따른_지역별_빈대_출몰_기사_수.png")
plt.show()

# 6. 히스토그램 생성 (키워드별 뉴스 개수)
df_histogram = pd.read_excel(excel_file, sheet_name=3)
norm = plt.Normalize(df_histogram['뉴스 개수'].min(), df_histogram['뉴스 개수'].max())
colors = plt.cm.Blues(norm(df_histogram['뉴스 개수']))

# 새로운 Figure와 Axes 생성
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(df_histogram['키워드'], df_histogram['뉴스 개수'], color=colors, edgecolor='black')

ax.set_title('장소별 빈대 출몰 횟수', fontsize=16)
ax.set_xlabel('키워드', fontsize=10)
ax.set_ylabel('뉴스 개수', fontsize=10)
ax.set_xticks(range(len(df_histogram['키워드'])))
ax.set_xticklabels(df_histogram['키워드'], rotation=45)

# Colorbar 추가
sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label('뉴스 개수', fontsize=10)

plt.tight_layout()
plt.savefig("장소별_빈대_출몰_횟수.png")
plt.show()

# 7. 한국 지도 그리기 (Matplotlib)
map = Basemap(
    projection='merc',
    llcrnrlat=33.0,
    urcrnrlat=38.6,
    llcrnrlon=124.0,
    urcrnrlon=130.5,
    resolution='i'
)

map.drawcoastlines()
map.drawcountries()
map.drawrivers(color='blue')
map.drawmapboundary(fill_color='lightblue')
map.fillcontinents(color='lightgreen', lake_color='lightblue')

scatter = None
df_bar = df_bar[['지역', '횟수']]
for _, row in df_bar.iterrows():
    region = row['지역']
    count = row['횟수']
    if region in locations:
        lat, lon = locations[region]
        x, y = map(lon, lat)
        color = get_color(count)
        scatter = map.scatter(x, y, marker='o', color=color, s=100)
        plt.text(x + 5000, y + 5000, f"{region} ({count})", fontsize=9, ha='left', color=color)

plt.title("23.10.13-11.30 한국 빈대 출몰 횟수", fontsize=16)
legend_labels = [
    ("1-10", "green"),
    ("11-20", "yellow"),
    ("21-30", "orange"),
    ("30 이상", "red")]

legend_handles = [mpatches.Patch(color=color, label=label) for label, color in legend_labels]
plt.legend(handles=legend_handles, loc='lower left', title="횟수 범위")
plt.savefig("한국_빈대_출몰_횟수.png")
plt.show()

# 8. 날짜별 기사 개수 꺾은선 그래프 생성
date_counts, date_counts2 = [], []
for file_path in file_paths:
    df = pd.read_csv(file_path)
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d')
    counts = df['날짜'].value_counts().sort_index()
    date_counts.append(counts)

for file_path in file_paths2:
    df = pd.read_csv(file_path)
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d')
    counts = df['날짜'].value_counts().sort_index()
    date_counts2.append(counts)

merged_counts = pd.concat(date_counts, axis=1)
merged_counts2 = pd.concat(date_counts2, axis=1)
merged_counts.columns = ['23년 9월', '23년 10월', '23년 11월']
merged_counts2.columns = ['24년 9월', '24년 10월', '24년 11월']
merged_counts = merged_counts.fillna(0)
merged_counts2 = merged_counts2.fillna(0)

plt.figure(figsize=(12, 6))
for column in merged_counts.columns:
    plt.plot(merged_counts.index, merged_counts[column], marker='o', label=column, linestyle='-', linewidth=2)

plt.title('23년도 9-11월 빈대 기사 빈도', fontsize=16)
plt.xlabel('날짜', fontsize=10)
plt.ylabel('기사 개수', fontsize=10)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.legend(title='월별', fontsize=10)
plt.grid(alpha=0.5, linestyle='--')
plt.tight_layout()
plt.savefig("23_9_11월_빈대_기사_빈도.png")

plt.figure(figsize=(12, 6))
for column in merged_counts2.columns:
    plt.plot(merged_counts2.index, merged_counts2[column], marker='o', label=column, linestyle='-', linewidth=2)

plt.title('24년도 9-11월 빈대 기사 빈도', fontsize=16)
plt.xlabel('날짜', fontsize=10)
plt.ylabel('기사 개수', fontsize=10)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.legend(title='월별', fontsize=10)
plt.grid(alpha=0.5, linestyle='--')
plt.tight_layout()
plt.savefig("24_9_11월_빈대_기사_빈도.png")

plt.show()