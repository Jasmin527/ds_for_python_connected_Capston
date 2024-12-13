from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

try:
    # WebDriver 초기화
    browser = webdriver.Chrome()

    # "빈대 확인" 키워드로 크롤링
    keyword = "%EB%B9%88%EB%8C%80+%ED%99%95%EC%9D%B8"

    # 10월 13일부터 11월 30일까지의 기사만 포함
    start_month, end_month = 10, 11
    days_range = {
        10: range(13, 32),  # 10월 13일부터 10월 말까지
        11: range(1, 31),   # 11월 1일부터 11월 30일까지
    }

    # 기사 데이터 저장을 위한 딕셔너리
    data = {'날짜': [], '번호': [], '뉴스 제목': []}

    for month in range(start_month, end_month + 1):
        for day in days_range[month]:
            formatted_month = f"{month:02d}"
            formatted_day = f"{day:02d}"

            # 검색 URL 설정
            url = (f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=2&photo=0"
                   f"&field=0&pd=3&ds=2023.{formatted_month}.{formatted_day}&de=2023.{formatted_month}.{formatted_day}"
                   f"&mynews=1&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0")

            article_number = 1  # 기사 번호 초기화

            while True:
                browser.get(url)
                time.sleep(2)

                # 페이지 끝까지 스크롤
                last_height = browser.execute_script("return document.body.scrollHeight")
                while True:
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # HTML 파싱
                html = browser.page_source
                soup = BeautifulSoup(html, "html.parser")

                # 기사 제목 추출
                name_list = soup.select('a.news_tit')

                if not name_list:
                    print(f"2023.{formatted_month}.{formatted_day}에서 더 이상 기사 데이터를 찾을 수 없습니다.")
                    break

                for i in name_list:
                    date_str = f"2023.{formatted_month}.{formatted_day}"
                    title = i.get_text().strip()

                    # 데이터 저장
                    data['날짜'].append(date_str)
                    data['번호'].append(article_number)
                    data['뉴스 제목'].append(title)

                    article_number += 1

                print(f"2023.{formatted_month}.{formatted_day}에서 기사를 모두 수집했습니다.")
                break

    # DataFrame으로 변환
    df = pd.DataFrame(data)

    # CSV 저장
    csv_filename = "2023_빈대_확인.csv"
    df.to_csv(csv_filename, encoding='utf-8-sig', index=False)
    print(f"[크롤링 완료] 저장된 파일: {csv_filename}")

except Exception as e:
    print("에러 발생:", e)

finally:
    if 'browser' in locals():
        browser.quit()