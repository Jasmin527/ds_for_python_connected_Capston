# 🐞 파이썬을 이용한 데이터사이언스_캡스톤디자인 연계실습 🐞

<div align> 
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white">
</div align> 

&nbsp;

## 👥 Members
**[데이터사이언스학과_3조]** <br/>
**2023111781_김지우 / 2023111784_노주원 / 2023111809_장예서**

&nbsp;

##  🔎 Research subject
#### [Background]


|신체적 • 정신적 영향|빈대의 재등장|국가 대응 미흡|
|-----|-----|-----|

  ⇒ 개인적 및 사회적 영향이 크고 문제 해결이 필요하다고 판단

&nbsp;
#### [Causes_analysis]

|시기적 영향|빈대의 특성|현황|
|-----|-----|-----|
|• 글로벌 이동|• 빠른 번식, 살충제 내성 |• 관련 지식 부족|

&nbsp;

## 💡 Solution (original ver.)
### [개발 및 어플리케이션 이용] : 
|빈대 O/X 알고리즘|빈대 출몰 위치 도표|
|------|------|


#### 1. 빈대 물림 자국 여부 판별 알고리즘
- bedbug_correct_img = 400장 (bedbug)
- bedbug_incorrect_img = 400장 (ant, mosquito, spider)
- (캡스톤디자인_1) Teachable Machine Application 사용

<br>

- 크롤링한 데이터 전처리는 정확한 사진 선택 (신뢰성 확보)
- 개체 별(bedbug_correct, bedbug_incorrect) 개수 통일 (과적합 방지)
- 이미지 확대 및 방향 회전, 밝기 조절 별도 적용 (정확도 상승)

#### 2. 빈대 출몰 위치 도표
- 선정 키워드 = '빈대 출몰', '빈대 확인'
- 수집 기간 = 23.10.13 (빈대 재등장 시점) ~ 23.11.30 <br/>
- 뉴스 제목 크롤링
- CSV 파일 불러오기 및 도/시/구 분류
- 도표 제작 

&nbsp;

### [웹사이트 사용] : 
|빈대 세부사항|Q&A 활성화|
|------|------|


#### 3. 빈대 세부사항
- 빈대 정보 요약
  - 질병 관리청, 환경부, 서울시 감염병 연구센터, 서울시에서 제공하는 정보 등을 병합해서 볼 수 있는 페이지 제공

#### 4. Q&A 서비스 제공
- 사이트 이용자들이 자유롭게 서로 질의응답하고 더 다양하게 정보를 얻어갈 수 있는 게시판 운영하는 페이지 제작
- **e.g.) 빈대 사진 구분, 빈대 관련 정보 질문, 사이트 관련 질문** <br/>
(1) 어제부터 계속 간지러운데 혹시 이런 자국 있으면 빈대한테 물린걸까요? <br/>
(2) 빈대 관련 기사 보고 무서워서 살균 업체를 부르려고 하는데 잘하는 곳 있나요? (노원구 내) <br/>
(3) 살충제를 살까 하는데 이 살충제 쓰시는 분 계시나요? 집에 아이가 있어서 고민이 되네요..<br/>
(4) 빈대 피해가 심각한데 정부가 하는 일이 무엇인지 ... 관련 계획 정리해둔거 있을까요? <br/>

&nbsp;

## 📈 Develop
**[Crawling]**
- 기존 네이버 뉴스 (페이지 수 제공) 형식 → 페이지 구분 없이 스크롤 하는 방식으로 업데이트 <br/>
   → 그에 맞게 text_crawling 코드 수정
- 2023년 09월 ~ 11월 vs. 2024년 09월 ~ 11월 compare (빈대 언급 빈도)

<br>

**[Visualization]**
- 지역별 빈대 피해 발생 빈도 (지도를 활용한 시각화) <br/>
- 장소 별 발생 횟수 (고시원, 지하철 등 공공장소) <br/>
- 빈대 출몰 기사 민감도 (text_preprocessing_part에서 count한 기사 개수 그래프로 시각화)
- 날짜 별 기사 증가량 (2023년도와 2024년도의 기사 증가량)

<br>

**[Preprocessing]**
- 이전에 수집했던 img, text data 전처리 진행 <br/>

**(1) image**
  - 중복 사진 제거 (해상도, 날짜, 크기 등 비교 후 판단하도록 설계)
  - 손상된 이미지 파일 제거
  - 최종 이미지 개수 출력
  - 이미지 별 크기 정규화
  - 데이터 증강 (밝기 조절, 방향 회전)
  - 이상치 제거
  ⇒ 모두 진행 후 최종 전처리된 데이터는 별도 폴더에 새롭게 저장

**(2) text**
  - 빈대가 출몰하는 장소의 키워드를 추출한 후 장소 별 발생 횟수 측정
  - 같은 날 언급된 경우의 중복 횟수 전처리
  - 빈대 출몰 민감도 (개수 count) <br/>
    : 같은 주제의 기사의 개수 多, 해당 이슈에 대해 민감하게 반응하고 있음 의미 <br/>

<br>

**[Modelling]**
- 크롤링을 통해 얻었던 '빈대_확인', '빈대_신고' 관련 기사를 bar-graph와 word-cloud로 추이 분석 <br/>

**(1) bar-graph**
  - 뉴스 제목의 길이를 측정하여 2023년과 2024년 뉴스의 텍스트 분석 진행
  - 뉴스 기사의 주요 정보가 압축 또는 길게 설명되었는지 파악하여 패턴 분석

**(2) word-cloud**
  - 2023년/2024년에 뉴스에서 가장 많이 출현된 단어를 파악 (단어 빈도 분석)
  - 단어 빈도 분석을 통해 그 당시 중요하게 생각했던 요소들을 파악 및 비교 가능

&nbsp;

## 🍀 Resource
****[image_crawling_link]****<br/>
[bedbug_img](https://search.naver.com/search.naver?ssc=tab.image.all&where=image&sm=tab_jum&query=%EB%B9%88%EB%8C%80) <br/>
[ant_img](https://search.naver.com/search.naver?sm=tab_hty.top&where=image&ssc=tab.image.all&query=%EA%B0%9C%EB%AF%B8&oquery=%EA%B1%B0%EB%AF%B8&tqi=i2Z0%2BdpzL8wssiSiTSVssssssSw-138964)<br/>
[mosquito_img](https://search.naver.com/search.naver?sm=tab_hty.top&where=image&ssc=tab.image.all&query=%EB%AA%A8%EA%B8%B0&oquery=%EC%A7%84%EB%93%9C%EA%B8%B0&tqi=i2Z1awpzL8wssi4%2BHmsssssssd0-253630)<br/>
[tick_img](https://search.naver.com/search.naver?sm=tab_hty.top&where=image&ssc=tab.image.all&query=%EC%A7%84%EB%93%9C%EA%B8%B0&oquery=%EA%B0%9C%EB%AF%B8&tqi=i2Z0%2FlqVOswsshRGwkwssssssmd-101476)<br/>

<br>

****[text_crawling_link]****<br/>
[2023_bedbug_check](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80%20%ED%99%95%EC%9D%B8&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2023.10.13&de=2023.10.13&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20231013to20231013&is_sug_officeid=0&office_category=0&service_area=0) <br/>
[2023_bedbug_declaration](https://search.naver.com/search.naver?sm=tab_hty.top&where=news&ssc=tab.news.all&query=%EB%B9%88%EB%8C%80+%EC%8B%A0%EA%B3%A0&oquery=%EB%B9%88%EB%8C%80+%ED%99%95%EC%9D%B8&tqi=i2Z2dwqo1fsss6sMid0ssssssYR-349873&nso=so%3Ar%2Cp%3Afrom20231013to20231013&de=2023.10.13&ds=2023.10.13&mynews=0&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&service_area=0&sort=2) <br/>
[2024_bedbug_check](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80%20%ED%99%95%EC%9D%B8&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2024.09.01&de=2024.11.30&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20240901to20241130&is_sug_officeid=0&office_category=0&service_area=0) <br/>
[2024_bedbug_declaration](https://search.naver.com/search.naver?sm=tab_hty.top&where=news&ssc=tab.news.all&query=%EB%B9%88%EB%8C%80+%EC%8B%A0%EA%B3%A0&oquery=%EB%B9%88%EB%8C%80+%ED%99%95%EC%9D%B8&tqi=i2Z3wdqo1e8ssi7341ossssstUd-088255&nso=so%3Ar%2Cp%3Afrom20240901to20241130&de=2024.11.30&ds=2024.09.01&mynews=0&office_category=0&office_section_code=0&office_type=0&pd=3&photo=0&service_area=0&sort=2) <br/>
[2023_09_bedbug](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2023.09.01&de=2023.09.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20230901to20230901&is_sug_officeid=0&office_category=0&service_area=0) <br/>
[2023_10_bedbug](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2023.10.01&de=2023.10.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20231001to20231001&is_sug_officeid=0&office_category=0&service_area=0) <br/>
[2023_11_bedbug](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2023.11.01&de=2023.11.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20231101to20231101&is_sug_officeid=0&office_category=0&service_area=0) <br/>
[2024_09_bedbug](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2024.09.01&de=2024.09.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20240901to20240901&is_sug_officeid=0&office_category=0&service_area=0)<br/>
[2024_10_bedbug](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2024.10.01&de=2024.10.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20241001to20241001&is_sug_officeid=0&office_category=0&service_area=0) <br/>
[2024_11_bedbug](https://search.naver.com/search.naver?where=news&query=%EB%B9%88%EB%8C%80&sm=tab_opt&sort=2&photo=0&field=0&pd=3&ds=2024.11.01&de=2024.11.01&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20241101to20241101&is_sug_officeid=0&office_category=0&service_area=0) <br/>

&nbsp;

## 🗓️ Schedule
```23.11.19```
- 깃허브 기본 세팅
- 캡스톤 디자인 리마인드

<br>

```23.11.25```
- 디벨롭 아이디어 제안 (전처리, 시각화)
- 기존에 가지고 있던 엑셀 파일 응용 방법 회의

<br>

```23.11.28```
- 각자 설계한 코드 피드백 진행
- 시각화 아이디에이션 (파이썬 내에서 시각화하는 방법 vs 웹브라우저에서 시각화하는 방법)
  ⇒ 두 가지 버전으로 만들기 결정
  
<br>

```23.11.29```
- 모델링 방법 회의 (딥러닝 사용 여부)
- 시각화 코드 1차 작성
- 전처리 코드 1차 작성

<br>

```23.12.04```
- 빈도분석 아이디어 회의 (키워드 추출, 건 수 카운팅 etc.)
- 디벨롭한 코드 설명 및 피드백 (이미지 전처리, 텍스트 전처리, 기사 추가 크롤링)
  
<br>

```23.12.11```
- 변경된 '네이버' 기사 페이지 기능 (페이지 수 → 스크롤)을 고려한 새 크롤링 코드 완성
- 현황 비교를 위한 24년도 크롤링 코드 실행

<br>

```23.12.14```
- 각자 실습 코드 push
- 시각화 코드 디벨롭
- 전처리 코드 완성

<br>

```23.12.16```
- 모든 branch 코드 master에 merge
- 변수명 통일, 파일 명 변경 (eng ver.), 주석 다듬기 (세부적으로 작성) 등
- 시각화 코드 추합
- 이전 크롤링 코드 업로드 (캡스톤디자인1_mosquito, ant, tick, bedbug 총 4개 생성)

<br>

```23.12.17```
- 깃허브 파일 정리 및 최종 수정
