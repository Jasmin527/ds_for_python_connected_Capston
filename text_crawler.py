#키워드 '빈대' 네이버 뉴스 크롤링 코드
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

try:
    #WebDriver 초기화 과정 가지기
    browser = webdriver.Chrome()

    #23년도 빈대 주요 발생 기간과 1년이 지난 후 24년도의 같은 기간 설정하기
    #23년도 9, 10, 11월과 24년도 9, 10, 11월
    periods = ["2023.09", "2023.10", "2023.11", "2024.09", "2024.10", "2024.11"]
    
    for period in periods: 
        year, month = period.split('.')

        #기사 데이터(기사 작성 날짜, 날짜당 기사 개수, 뉴스 제목)를 저장하는 딕셔너리 생성하기
        data = {'날짜': [], '번호': [], '뉴스 제목': []}

        for day in range(1, 32):  #10월의 경우 31일까지 있는 점을 고려하여 최대 31일까지 돌 수 있도록 32까지 지정
            #10 미만의 한자리 수n의 경우 날짜에 0n으로 표시가 됨
            #따라서 한자리 수의 경우 0 텍스트를 붙여주고, 10 이상일 경우 그대로 진행할 수 있는 if문 작성하기
            if day < 10:
                formatted_day = f"0{day}"
            else:
                formatted_day = str(day)

            #빈대 키워드를 검색했을 때 날짜 값을 제외한 나머지 링크는 같다는 점을 고려하여 기본 URL 틀 설정하기.
            url = (f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%B9%88%EB%8C%80&sort=2&photo=0"
                   f"&field=0&pd=3&ds={period}.{formatted_day}&de={period}.{formatted_day}&mynews=1&office_type=0&"
                   f"office_section_code=0&news_office_checked=&office_category=0&service_area=0")

            article_number = 1  #기사 번호 초기화하기

            while True:  #스크롤을 통하여 모든 기사 DATA를 가져올 수 있게하는 while문
                browser.get(url)
                time.sleep(2)  #페이지 로딩이 원활하게 되도록 2초의 시간을 줌.

                #페이지 끝까지 확인할 수 있게 스크롤하는 동작 실행하기
                last_height = browser.execute_script("return document.body.scrollHeight")
                while True:
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)  #스크롤 후 새 정보를 원활하게 받아오기 위해서 1초의 시간을 줌.
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                #HTML 파싱 과정 가지기
                html = browser.page_source
                soup = BeautifulSoup(html, "html.parser")

                #기사 제목을 추출하기
                name_list = soup.select('a.news_tit')

                if not name_list:  #만약 날짜를 바꿔서 검색했을 때 기사 목록이 없다면 그 다음날로 날짜 변경하도록 break
                    print(f"{period}.{formatted_day}에서 더 이상 기사 데이터를 찾을 수 없습니다.")
                    break

                for i in name_list:
                    date_str = f"{period}.{formatted_day}"
                    title = i.get_text().strip()

                    #각 칼럼 별로 데이터 값을 저장하기
                    data['날짜'].append(date_str)
                    data['번호'].append(article_number)
                    data['뉴스 제목'].append(title)

                    article_number += 1 
                    #하나의 기사를 저장한 후 기사 번호에 +1하여 카운트 하기

                #날짜별 모든 기사 탐색이 완료되었다면, 반복 종료하고 알리기
                print(f"{period}.{formatted_day}에서 기사를 모두 수집했습니다.")
                break

        #DataFrame으로 변환하는 과정 거치기
        df = pd.DataFrame(data)

        #dataframe을 CSV로 저장하기
        csv_filename = f"{year}년_{month}월_빈대.csv"
        df.to_csv(csv_filename, encoding='utf-8-sig', index=False)
        print(f"크롤링 완료! 저장된 파일: {csv_filename}")

except Exception as e:
    print("에러 발생:", e)

finally:
    if 'browser' in locals():
        browser.quit() 
        #다 종료된 후 브라우저에서 나가기
