# 🐞 파이썬을 이용한 데이터사이언스_캡스톤디자인 연계실습 🐞

<div align> 
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white">
</div align> 

&nbsp;

## Members
**[데이터사이언스학과]**

**2023111781_김지우 / 2023111784_노주원 / 2023111809_장예서**

&nbsp;

##  Research subject
#### [Background]


|신체적 • 정신적 영향|빈대의 재등장|국가 대응 미흡|
|-----|-----|-----|

  ⇒ 개인적 및 사회적 영향이 크고 문제 해결이 필요하다고 판단


#### [Cause analysis]


|시기적 영향|빈대의 특성|현황|
|-----|-----|-----|
|글로벌 이동|빠른 번식, 살충제 내성|관련 지식 부족|

&nbsp;

## Solution (original ver.)
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

<br>

- **e.g.) 빈대 사진 구분, 빈대 관련 정보 질문, 사이트 관련 질문** <br/>
(1) 어제부터 계속 간지러운데 혹시 이런 자국 있으면 빈대한테 물린걸까요? <br/>
(2) 빈대 관련 기사 보고 무서워서 살균 업체를 부르려고 하는데 잘하는 곳 있나요? (노원구 내) <br/>
(3) 살충제를 살까 하는데 이 살충제 쓰시는 분 계시나요? 집에 아이가 있어서 고민이 되네요..<br/>
(4) 빈대 피해가 심각한데 정부가 하는 일이 무엇인지 ... 관련 계획 정리해둔거 있을까요? <br/>


## Develop
**[Crawling]**
- 기존 네이버 뉴스 (페이지 수 제공) 형식 → 페이지 구분 없이 스크롤 하는 방식으로 업데이트 <br/>
   → 그에 맞게 text_crawling 코드 수정
- 2023년 09월 ~ 11월 vs. 2024년 09월 ~ 11월 compare (빈대 언급 빈도)

<br>

**[Visualization]**
- 지역별 빈대 피해 발생 빈도 (지도를 활용한 시각화) <br/>
- 장소 별 발생 횟수 (고시원, 지하철 등 공공장소) <br/>
- 빈대 출몰 기사 민감도 (text_preprocessing_part에서 count한 기사 개수 그래프로 시각화)
- 날짜 별 기사 증가량

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

![Languages](https://img.shields.io/github/languages/top/{Jasmin527}/{https://github.com/Jasmin527/ds_for_python_connected_Capston.git})
![Contributors](https://img.shields.io/github/contributors/{Jasmin527}/{https://github.com/Jasmin527/ds_for_python_connected_Capston.git})
