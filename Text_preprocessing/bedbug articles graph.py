import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows의 맑은 고딕 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 파일 경로 설정
file_paths = [
    "2023년_09월_빈대_출몰.csv",
    "2023년_10월_빈대_출몰.csv",
    "2023년_11월_빈대_출몰.csv"
]

# 데이터 수집
date_counts = []
for file_path in file_paths:
    # CSV 파일 로드
    df = pd.read_csv(file_path)

    # 날짜 형식 변환 (2023.09.01 형식)
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y.%m.%d')  # 형식을 점(.)으로 구분된 형식으로 수정

    # 날짜별 기사 개수 집계
    counts = df['날짜'].value_counts().sort_index()
    date_counts.append(counts)

# 모든 데이터프레임 병합
merged_counts = pd.concat(date_counts, axis=1)
merged_counts.columns = ['9월', '10월', '11월']
merged_counts = merged_counts.fillna(0)  # NaN 값은 0으로 대체

# 꺾은선 그래프 생성
plt.figure(figsize=(12, 6))
for column in merged_counts.columns:
    plt.plot(merged_counts.index, merged_counts[column], marker='o', label=column, linestyle='-', linewidth=2)

# 그래프 꾸미기
plt.title('날짜별 기사 개수 비교 (빈대 출몰)', fontsize=16)
plt.xlabel('날짜', fontsize=14)
plt.ylabel('기사 개수', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.legend(title='월별', fontsize=12)
plt.grid(alpha=0.5, linestyle='--')

# 그래프 저장 및 표시
output_image = "날짜별_기사_개수_꺾은선그래프.png"
plt.tight_layout()
plt.savefig(output_image)
plt.show()

print(f"꺾은선 그래프가 저장되었습니다: {output_image}")