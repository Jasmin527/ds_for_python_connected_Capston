import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# matplotlib 시각화 한글 깨짐 방지
plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우: 맑은 고딕
plt.rcParams['axes.unicode_minus'] = False

# CSV 파일 불러오기
df_2023 = pd.read_csv("text_crawling/2023_빈대_확인.csv")
df_2024 = pd.read_csv("text_crawling/2024_빈대_확인.csv")

# 날짜를 datetime 형식으로 변환 (날짜 형식 'yyyy.mm.dd' 처리)
df_2023['날짜'] = pd.to_datetime(df_2023['날짜'], format='%Y.%m.%d', errors='coerce')
df_2024['날짜'] = pd.to_datetime(df_2024['날짜'], format='%Y.%m.%d', errors='coerce')

# NaN 날짜 값 제거
df_2023 = df_2023.dropna(subset=['날짜'])
df_2024 = df_2024.dropna(subset=['날짜'])

# 1. 제목 길이 분석 (뉴스 제목 컬럼 가정)
if '뉴스 제목' in df_2023.columns and '뉴스 제목' in df_2024.columns:
    # 제목 길이 계산
    df_2023['제목 길이'] = df_2023['뉴스 제목'].apply(len)
    df_2024['제목 길이'] = df_2024['뉴스 제목'].apply(len)

    # 제목 길이 통계
    print("2023년 뉴스 제목 길이 통계:\n", df_2023['제목 길이'].describe())
    print("\n2024년 뉴스 제목 길이 통계:\n", df_2024['제목 길이'].describe())

    # 제목 길이 히스토그램
    plt.figure(figsize=(10, 6))
    plt.hist(df_2023['제목 길이'], bins=20, alpha=0.5, label="2023년", color='lightcoral')
    plt.hist(df_2024['제목 길이'], bins=20, alpha=0.5, label="2024년", color='lightblue')
    plt.xlabel("제목 길이")
    plt.ylabel("빈도수")
    plt.title("2023년과 2024년 뉴스 제목 길이 비교")
    plt.legend()
    plt.show()

# 2. 단어 빈도 분석
if '뉴스 제목' in df_2023.columns and '뉴스 제목' in df_2024.columns:
    custom_stop_words = ['그리고', '그러나', '그래서', '하지만', '저는', '우리는', '당신은', '이것은']  # 불용어 목록

    # 2023년 단어 분석
    vectorizer_2023 = CountVectorizer(stop_words=custom_stop_words)
    word_count_2023 = vectorizer_2023.fit_transform(df_2023['뉴스 제목'])
    word_freq_2023 = Counter(dict(zip(vectorizer_2023.get_feature_names_out(), word_count_2023.toarray().sum(axis=0))))
    top_words_2023 = word_freq_2023.most_common(10)

    # 2024년 단어 분석
    vectorizer_2024 = CountVectorizer(stop_words=custom_stop_words)
    word_count_2024 = vectorizer_2024.fit_transform(df_2024['뉴스 제목'])
    word_freq_2024 = Counter(dict(zip(vectorizer_2024.get_feature_names_out(), word_count_2024.toarray().sum(axis=0))))
    top_words_2024 = word_freq_2024.most_common(10)

    # 출력
    print("\n2023년 뉴스에서 가장 많이 등장한 단어:\n", top_words_2023)
    print("\n2024년 뉴스에서 가장 많이 등장한 단어:\n", top_words_2024)


    # 워드클라우드 생성
    def plot_wordcloud(word_freq, title):
        wordcloud = WordCloud(
            font_path='C:/Windows/Fonts/malgun.ttf',  # 한글 폰트 경로
            width=800, height=400, background_color='white'
        ).generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title(title)
        plt.show()


    plot_wordcloud(word_freq_2023, "2023년 뉴스 제목 워드클라우드")
    plot_wordcloud(word_freq_2024, "2024년 뉴스 제목 워드클라우드")