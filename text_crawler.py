from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time

# 데이터 저장 딕셔너리 생성
data = {'날짜': [], '번호': [], '뉴스 제목': []}

# 브라우저 설정 및 드라이버 초기화
browser = webdriver.Chrome()

try:
    for day in range(1, 32):  # 날짜 반복
        # 날짜 포맷 처리
        if day < 10:
            formatted_day = f"0{day}"
        else:
            formatted_day = str(day)

        # URL 설정
        url = (f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%B9%88%EB%8C%80&sort=2&photo=0"
               f"&field=0&pd=3&ds=2023.10.{formatted_day}&de=2023.10.{formatted_day}&mynews=1&office_type=0&"
               f"office_section_code=0&news_office_checked=&office_category=0&service_area=0")

        article_number = 1  # 기사 번호 초기화

        while True:  # 스크롤링으로 모든 데이터 탐색
            browser.get(url)
            time.sleep(2)  # 페이지 로딩 대기

            # 스크롤 동작: 페이지 끝까지 스크롤
            last_height = browser.execute_script("return document.body.scrollHeight")
            while True:
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # 스크롤 후 대기
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # HTML 파싱
            html = browser.page_source
            soup = BeautifulSoup(html, "html.parser")

            # 기사 제목 추출
            name_list = soup.select('a.news_tit')

            if not name_list:  # 기사 목록이 없으면 날짜 변경
                print(f"2023.10.{formatted_day}에서 더 이상 기사 데이터를 찾을 수 없습니다.")
                break

            for i in name_list:
                date_str = f"2023.10.{formatted_day}"
                title = i.get_text().strip()

                # 데이터 저장
                data['날짜'].append(date_str)
                data['번호'].append(article_number)
                data['뉴스 제목'].append(title)

                article_number += 1

            # 모든 기사 탐색이 완료된 경우 반복 종료
            print(f"2023.10.{formatted_day}에서 기사를 모두 수집했습니다.")
            break

    # DataFrame으로 변환
    df = pd.DataFrame(data)

    # CSV로 저장
    df.to_csv('10월_빈대_출몰_스크롤.csv', encoding='utf-8-sig', index=False)
    print("크롤링 완료! 저장된 파일: 2023_10월_빈대_출몰.csv")

except Exception as e:
    print("에러 발생:", e)

finally:
    browser.quit()