from selenium import webdriver #Selenium을 이용한 웹 드라이버 제어
from bs4 import BeautifulSoup #HTML 파싱을 위한 BeautifulSoup
import pandas as pd #데이터 처리 및 저장을 위한 Pandas
import time #대기 시간을 설정하기 위한 time

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

    for month in range(start_month, end_month + 1): #시작 월부터 종료 월까지 반복
        for day in days_range[month]: #해당 월의 모든 날짜를 반복
            formatted_month = f"{month:02d}" #월을 2자리 숫자로 포맷 (예: 1 -> 01)
            formatted_day = f"{day:02d}" #일을 2자리 숫자로 포맷 (예: 1 -> 01)


            # 검색 URL 설정
            url = (f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=2&photo=0"
                   f"&field=0&pd=3&ds=2024.{formatted_month}.{formatted_day}&de=2024.{formatted_month}.{formatted_day}"
                   f"&mynews=1&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0")

            article_number = 1  # 기사 번호 초기화

            while True:
                browser.get(url)
                time.sleep(2)

                # 페이지 끝까지 스크롤
                last_height = browser.execute_script("return document.body.scrollHeight") #현재 페이지의 전체 스크롤 높이를 가져옴
                while True:
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #페이지 맨 아래로 스크롤
                    time.sleep(1) #스크롤 후 1초 대기 (페이지 로딩을 위해)
                    new_height = browser.execute_script("return document.body.scrollHeight") #스크롤 후 새로운 전체 높이를 가져옴
                    if new_height == last_height: #스크롤 전후 높이가 같으면 (더 이상 스크롤할 내용이 없으면)
                        break #종료
                    last_height = new_height #현재 높이를 마지막 높이로 업데이트

                # HTML 파싱
                html = browser.page_source
                soup = BeautifulSoup(html, "html.parser")

                # 기사 제목 추출
                name_list = soup.select('a.news_tit')

                if not name_list: #뉴스 기사가 없으면
                    print(f"2024.{formatted_month}.{formatted_day}에서 더 이상 기사 데이터를 찾을 수 없습니다.")
                    break

                for i in name_list: #name_list의 각 항목(i)을 반복
                    date_str = f"2023.{formatted_month}.{formatted_day}" #연도와 포맷된 월, 일을 결합해 날짜 문자열 생성
                    title = i.get_text().strip() #요소의 텍스트를 가져와 공백 제거 후 제목으로 저장

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
    csv_filename = "2024_bedbug_check.csv"
    df.to_csv(csv_filename, encoding='utf-8-sig', index=False)
    print(f"[크롤링 완료] 저장된 파일: {csv_filename}")

except Exception as e: #예외 발생 시 실행되는 블록
    print("에러 발생:", e) #발생한 에러 메시지를 출력

finally: #예외 발생 여부와 관계없이 항상 실행되는 블록
    if 'browser' in locals(): #'browser' 변수가 현재 로컬에 존재하면
        browser.quit() #브라우저를 종료
