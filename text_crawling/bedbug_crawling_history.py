from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

data = {'날짜': [], '번호': [], '뉴스 제목': []} #csv로 뽑아낼 데이터의 딕셔너리 칸 생성

browser = webdriver.Chrome()

for day in range (1,31): #날짜마다 출력하기 위한 for문

		#url을 설정하고 기준 날짜를 바꿔가는 과정에서 1~9는 01~09로 표기됨을 파악.
    #이에 10보다 작은 값은 n은 0n으로 재설정
    if day < 10:
        day = "0" + str(day)

    url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=%EB%B9%88%EB%8C%80%20%EC%B6%9C%EB%AA%B0&sort=2&photo=0&field=0&pd=3&ds=2023.11.{}&de=2023.11.{}&mynews=1&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from202311{}to202311{},a:all&start=".format(day,day,day,day)

    key_number, a= 1, 1
    for _ in range (1,11): #한 날짜의 최대 페이지 수 만큼 반복으로 돌려줌

        browser.get(url+str(key_number))
        time.sleep(1)

# html 정보를 긁기 위한 세팅
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")

        name_list = soup.select('div.news_contents > a.news_tit')

        for i in name_list[:10]: #네이버 뉴스의 한 페이지엔 최대 10개의 기사가 담김
            bug_day = "2023.11.{}".format(day) #날짜 저장
            bug_num = a #날짜별 n번째 기사임을 표시
            bug_title = i.get_text() #기사 제목 긁어오기

            data['날짜'].append(bug_day)
            data['번호'].append(bug_num)
            data['뉴스 제목'].append(bug_title)

            a += 1
        key_number += 10 #key 넘버가 10씩 증가하면 다음페이지로 넘어가는 key 넘버가 됨

# table 형식으로 만들기
df = pd.DataFrame(data)
# csv로 저장
df.to_csv('10월_빈대_출몰.csv', encoding = 'utf-8-sig', index=False)
#저장될 파일 설정 및 한글 파일이 꺠지지 않는 코드 작성, 인덱스 제거

print(df) #데이터 프레임 미리보기