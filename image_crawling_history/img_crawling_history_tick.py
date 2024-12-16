from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import os
import time

# 웹 크롤링을 위한 브라우저 설정
browser = webdriver.Chrome()

# 진드기 이미지를 검색한 URL
url = "https://search.naver.com/search.naver?ssc=tab.image.all&where=image&sm=tab_jum&query=%EC%A7%84%EB%93%9C%EA%B8%B0"

# 브라우저에서 URL 열기
browser.get(url)

# 웹 페이지 로딩 시간을 고려하여 5초 대기
time.sleep(5)

# 페이지 소스(html) 가져오기
html = browser.page_source
soup = BeautifulSoup(html, "html.parser")

# 진드기 이미지 태그 선택 (img 태그를 포함하는 요소 선택)
mites_image = soup.select("section div img")

# 이미지를 저장할 폴더 생성
if not os.path.exists("mites_img"):
    os.makedirs("mites_img")

# 이미지 다운로드 및 저장
for idx, img in enumerate(mites_image):
    try:
        # 이미지 URL 가져오기
        img_url = img['src']

        # 저장할 파일 이름 정의
        img_name = f"mites_img/mite_{idx + 1}.jpg"

        # 이미지 다운로드 및 파일 저장
        urllib.request.urlretrieve(img_url, img_name)
        print(f"Image {idx + 1} downloaded and saved as {img_name}")
    except Exception as e:
        # 에러 발생 시 메시지 출력
        print(f"Error downloading image {idx + 1}: {e}")

# 브라우저 종료
browser.quit()