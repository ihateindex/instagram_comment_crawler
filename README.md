# Instagram Comment Crawler 설치 가이드

## 1. Python 설치

- Python 3.8 이상 버전이 필요합니다
- https://www.python.org/downloads/ 에서 다운로드

## 2. 가상환경 생성 및 활성화

<!-- 디렉토리 생성 및 vs code 작업영역 만들고 터미널에서 진행 -->

python3 -m venv venv
source venv/bin/activate

## 3. 필요한 패키지 설치

pip install -r requirements.txt

## 4. env 파일 생성 및 환경 변수 설정

INSTAGRAM_ID={인스타그램 아이디}
INSTAGRAM_PW={인스타그램 비밀번호}

## 5. 인스타그램 게시물 URL 설정

crawling_comments.py 파일 내에서 변수명 POST_URL에 인스타그램 게시물 URL 설정 (15번 라인)

POST_URL={인스타그램 게시물 URL}

## 6. 저장할 파일명 설정

crawling_comments.py 파일 내에서 변수명 SAVE_PATH에 저장할 파일명 설정 (16번 라인)

SAVE_PATH={저장할 파일명}

## 7. 크롤링 실행

터미널에서 python crawling_comments.py 명령어 실행

## 8. 저장된 파일 확인

crawling_comments.py 파일 내에서 변수명 SAVE_PATH에 설정한 파일명으로 csv 파일 생성됨
