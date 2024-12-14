import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import rcParams
import folium
import webbrowser
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib import font_manager, rc

# 1. 한글 폰트 설정
rcParams['font.family'] = 'Malgun Gothic'  # 윈도우에서 기본적으로 지원하는 한글 폰트
rcParams['axes.unicode_minus'] = False  # 마이너스 기호도 제대로 표시되도록 설정

# 2. 엑셀 파일 경로 설정 및 읽기
excel_file = "C:/Users/kimjiwoo/Downloads/bed_bug_location.xlsx"  # 파일 경로

# 대시보드 생성
fig, axes = plt.subplots(4, 1, figsize=(15, 20))  # 3개의 시각화를 세로로 배치
fig.subplots_adjust(hspace=0.5)  # 그래프 사이에 간격 추가

# 1. 히트맵 생성 (지역별 빈도)
df_heatmap = pd.read_excel(excel_file, sheet_name=1)
pivot_df = df_heatmap.pivot_table(index='지역', values='횟수', aggfunc='sum', fill_value=0)
sns.heatmap(pivot_df, cmap='Reds', annot=True, fmt='d', linewidths=.5, cbar_kws={'label': '횟수'}, ax=axes[0])
axes[0].set_title('지역별 기사 횟수 히트맵', fontsize=16)
axes[0].set_xlabel('지역', fontsize=14)
axes[0].set_ylabel('지역', fontsize=14)

# 2. 막대그래프 생성 (날짜에 따른 지역별 빈도)
df = pd.read_excel(excel_file, sheet_name=3)
regions = df['지역']
counts = df['횟수']
axes[1].bar(regions, counts, color='skyblue', edgecolor='black')
axes[1].set_title('지역별 등장 횟수', fontsize=16)
axes[1].set_xlabel('지역', fontsize=14)
axes[1].set_ylabel('횟수', fontsize=14)
axes[1].tick_params(axis='x', rotation=45)

# 3. 히스토그램 생성 (키워드별 뉴스 개수)
df_histogram = pd.read_excel(excel_file, sheet_name=2)
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

# 4번째 시트에서 '지역'과 '횟수' 열만 추출
df = df[['지역', '횟수']]  # 필요한 '지역'과 '횟수' 정보만 가져오기

# 3. 지역별 위도, 경도 정보 정의
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
    "경상도": [34.8120, 126.3917],
    "제주특별자치도": [33.4996, 126.5312]  # 제주도의 위도, 경도 수정
}  # 각 지역의 위도와 경도를 사전 형태로 정의

# 4. 색상 구분을 위한 함수 정의 (횟수에 따른 색상 구분)
def get_color(value):
    if value <= 10:  # 횟수가 10 이하일 경우
        return "blue"  # 파란색
    elif 11 <= value <= 20:  # 횟수가 11~20일 경우
        return "green"  # 초록색
    elif 21 <= value <= 30:  # 횟수가 21~30일 경우
        return "yellow"  # 노란색
    elif 31 <= value <= 40:  # 횟수가 31~40일 경우
        return "orange"  # 주황색
    else:  # 횟수가 40 이상일 경우
        return "red"  # 빨간색

# 5. 지도 생성 (중심은 서울로 설정)
map_center = [37.5665, 126.9780]  # 서울특별시의 위도와 경도를 지도 중심으로 설정
map_display = folium.Map(location=map_center, zoom_start=8)  # Folium으로 지도 객체 생성, zoom_level은 8로 설정

# 6. 각 지역에 대한 점을 지도에 추가
for _, row in df.iterrows():  # 데이터프레임의 각 행을 반복하면서 처리
    region = row['지역']  # 지역 이름
    count = row['횟수']  # 횟수

    # 지역별 위도, 경도 정보 추출
    if region in locations:  # 해당 지역이 locations에 존재하면
        latitude, longitude = locations[region]  # 위도, 경도 정보 추출

        # 횟수에 따라 색상 결정
        color = get_color(count)  # 횟수에 맞는 색상 값 받아옴

        # 원형 마커 추가 (색상과 크기 설정)
        circle_marker = folium.CircleMarker(
            location=[latitude, longitude],  # 마커의 위치는 위도, 경도
            radius=15,  # 원 크기 설정 (기본 크기보다 크게 설정)
            color=color,  # 원 테두리 색상
            fill=True,  # 원 안을 채우기
            fill_color=color,  # 원 안 채우기 색상
            fill_opacity=0.7,  # 채우기 색상의 투명도 설정
            popup=f"{region} (횟수: {count})",  # 마커 클릭 시 팝업에 지역 이름과 횟수 표시
        ).add_to(map_display)  # 지도에 추가

        # 원 안에 횟수 표시
        folium.Marker(
            location=[latitude, longitude],  # 마커 위치는 동일
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: black; text-align: center; line-height: 20px;">{count}</div>'
            )  # 원 안에 횟수를 검정색으로 표시
        ).add_to(map_display)  # 지도에 추가

        # 지역 이름을 오른쪽에 표시 (텍스트 오른쪽으로 배치, 공백 확보)
        folium.Marker(
            location=[latitude, longitude],  # 마커 위치는 동일
            popup=region,  # 마커 클릭 시 지역 이름 표시
            icon=folium.DivIcon(
                html=f'<div style="font-size: 12px; color: {color}; white-space: nowrap; transform: translateX(40px);">{region}</div>'
            )  # 텍스트를 오른쪽으로 이동 (40px 공백)
        ).add_to(map_display)  # 지도에 추가

# 7. 범례 추가 (색상에 대한 범위 표시)
legend_html = """
      <div style="position: fixed;
                  bottom: 30px; left: 30px; width: 200px; height: 180px;
                  background-color: white; border:2px solid grey;
                  z-index: 9999; font-size: 14px; padding: 10px;">
        <b>색상 범례</b><br>
        <i style="background: blue; width: 20px; height: 20px; display: inline-block;"></i> 1-10 <br>
        <i style="background: green; width: 20px; height: 20px; display: inline-block;"></i> 11-20 <br>
        <i style="background: yellow; width: 20px; height: 20px; display: inline-block;"></i> 21-30 <br>
        <i style="background: orange; width: 20px; height: 20px; display: inline-block;"></i> 31-40 <br>
        <i style="background: red; width: 20px; height: 20px; display: inline-block;"></i> 40 이상
    </div>
"""
map_display.get_root().html.add_child(folium.Element(legend_html))  # 범례 추가

# 8. 지도 저장
map_file = "map_with_counts_and_names_and_values_in_circle_right_text_more_space.html"  # 저장할 파일 이름
map_display.save(map_file)  # 파일로 저장
print(f"지도가 {map_file} 파일에 저장되었습니다.")  # 저장 완료 메시지

# 9. 브라우저에서 지도 열기
webbrowser.open(map_file)  # 브라우저에서 지도 열기

# 10. 지도 그리기 (Matplotlib으로 한국 지도 그리기)
# 한국 지도 범위 설정
map = Basemap(
    projection='merc',
    llcrnrlat=33.0,
    urcrnrlat=38.6,
    llcrnrlon=124.0,
    urcrnrlon=130.5,
    resolution='i'
)

# 지도 배경 그리기
map.drawcoastlines()
map.drawcountries()
map.drawrivers(color='blue')
map.drawmapboundary(fill_color='lightblue')
map.fillcontinents(color='lightgreen', lake_color='lightblue')

# 각 지역에 대한 점 그리기
scatter = None  # scatter 객체 초기화
for _, row in df.iterrows():
    region = row['지역']
    count = row['횟수']

    # 지역별 위도, 경도 좌표 확인
    if region in locations:
        lat, lon = locations[region]

        # 위도, 경도 값을 Basemap 좌표로 변환
        x, y = map(lon, lat)

        # 점 그리기
        color = get_color(count)
        scatter = map.scatter(x, y, marker='o', color=color, s=100)

        # 점 옆에 지역 이름과 횟수 표시 (점 바로 옆에 위치하도록 텍스트 추가)
        plt.text(x + 5000, y + 5000, f"{region} ({count})", fontsize=9, ha='left', color=color)

# 제목 및 범례 추가
plt.title("bedbug_location")  # 제목 변경

# 범례 추가
legend_labels = [
    ("1-10", "blue"),
    ("11-20", "green"),
    ("21-30", "yellow"),
    ("31-40", "orange"),
    ("40 이상", "red")
]

# 범례 객체 생성
legend_handles = [mpatches.Patch(color=color, label=label) for label, color in legend_labels]

# 범례 추가
plt.legend(handles=legend_handles, loc='lower left', title="횟수 범위")
# 최종 결과 확인
# 대시보드 저장 및 표시
output_image = "대시보드_지역_키워드_히트맵.png"
plt.savefig(output_image)
plt.show()