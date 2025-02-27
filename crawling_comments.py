from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# 🔹 크롤링 변수 설정
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")  # 환경 변수에서 아이디 가져오기
INSTAGRAM_PW = os.getenv("INSTAGRAM_PW")  # 환경 변수에서 비밀번호 가져오기
POST_URL = ""  # 크롤링할 인스타그램 게시물 URL
SAVE_PATH = "instagram_comments"  # 저장할 파일명

# 🔹 Chrome 실행
driver = webdriver.Chrome()

# 🔹 인스타그램 로그인 페이지로 이동
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)  # 페이지 로드 대기

# 🔹 아이디와 비밀번호 입력
username_input = driver.find_element(By.NAME, "username")
username_input.send_keys(INSTAGRAM_ID)
password_input = driver.find_element(By.NAME, "password")
password_input.send_keys(INSTAGRAM_PW)

# 🔹 엔터 키로 로그인
password_input.send_keys(Keys.RETURN)
time.sleep(5)  # 로그인 후 대기

# 🔹 게시물 페이지로 이동
driver.get(POST_URL)
time.sleep(5)  # 페이지 로드 대기

# 🔹 댓글 스크롤 영역 찾기
try:
    comment_scroll_area = driver.find_element(By.CLASS_NAME, "x5yr21d.xw2csxc.x1odjw0f.x1n2onr6")
    print("✅ 댓글 스크롤 영역 찾음!")
    
    # 🔹 댓글 컨테이너 정의
    comment_container = driver.find_element(By.CSS_SELECTOR, "div.x9f619.x78zum5.xdt5ytf.x5yr21d.xexx8yu.x1pi30zi.x1l90r2v.x1swvt13.x10l6tqk.xh8yej3 > div.x78zum5.xdt5ytf.x1iyjqo2")
except:
    print("❌ 댓글 스크롤 영역을 찾을 수 없습니다.")
    driver.quit()
    exit()

# 🔹 댓글 스크롤을 내려서 최대한 많은 댓글 로드
def scroll_comment_section():
    last_height = driver.execute_script("return arguments[0].scrollHeight", comment_scroll_area)
    no_change_count = 0  # 높이 변화가 없는 횟수를 추적
    
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_scroll_area)
        time.sleep(1)  # 로딩 대기 시간
        new_height = driver.execute_script("return arguments[0].scrollHeight", comment_scroll_area)
        
        if new_height == last_height:
            no_change_count += 1
            
            # 여러 번(3번) 연속으로 높이 변화가 없을 때만 종료
            if no_change_count >= 3:
                print("더 이상 스크롤할 내용이 없습니다.")
                break
            
            # 추가 시도: 약간의 위로 스크롤했다가 다시 아래로 스크롤
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight - 500", comment_scroll_area)
            time.sleep(1)
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_scroll_area)
            time.sleep(2)
        else:
            no_change_count = 0  # 높이가 변했으면 카운터 초기화
            
        last_height = new_height
        
        # 진행 상황 로그
        print(f"현재 스크롤 높이: {new_height}")

scroll_comment_section()

# 🔹 댓글 추출
all_comments = []
try:
    print("댓글 요소 찾기")
    comment_elements = comment_container.find_elements(By.CSS_SELECTOR, 
        "div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6 div.x78zum5.xdt5ytf.x1iyjqo2")
    
    if not comment_elements:
        print("❌ 댓글 요소를 찾을 수 없습니다.")
    
    for comment_element in comment_elements:
        try:
            # 상위로 올라가면서 사용자 이름이 있는 요소 찾기
            wrapper = comment_element.find_element(By.CSS_SELECTOR, "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1")
            username = wrapper.find_element(By.CSS_SELECTOR, "span._aade").text.strip()
            
            # 댓글 텍스트를 CSS 선택자로 추출
            comment = wrapper.find_element(By.CSS_SELECTOR, "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1cy8zhl.x1oa3qoh.x1nhvcw1 > span.x1lliihq.x1plvlek.xryxfnj").text.strip()
            
            # 시간 정보 찾기
            time_element = wrapper.find_element(By.CSS_SELECTOR, "time")  # CSS 선택자로 시간 요소 찾기
            timestamp = time_element.get_attribute("datetime")  # datetime 속성 추출
            
            if username and comment and not any(skip in comment for skip in ["답글", "좋아요"]):
                all_comments.append({
                    "username": username,
                    "comment": comment,
                    "timestamp": timestamp
                })
                
        except Exception as e:
            # print(f"댓글 처리 중 오류: {e}")
            continue

except Exception as e:
    print(f"전체 처리 중 오류: {e}")

# 🔹 크롤링한 댓글 데이터 출력
if all_comments:  # 'comments'를 'all_comments'로 수정
    print(f"✅ 총 {len(all_comments)}개의 댓글을 가져왔습니다.")
else:
    print("❌ 댓글을 찾을 수 없습니다.")

for idx in range(len(all_comments)):  # 'comments'를 'all_comments'로 수정
    username = all_comments[idx]['username'] if idx < len(all_comments) else "Unknown"
    comment_text = all_comments[idx]['comment'] if idx < len(all_comments) else "No Comment"
    timestamp = all_comments[idx]['timestamp'] if idx < len(all_comments) else "Unknown Time"
    
    # print(f"{idx + 1}. [{username}] ({timestamp}): {comment_text}")

# 🔹 크롬 종료
driver.quit()

# 댓글 데이터를 DataFrame으로 변환
df = pd.DataFrame(all_comments)

# CSV 파일로 저장
df.to_csv(f'{SAVE_PATH}.csv', index=False, encoding='utf-8-sig')  # utf-8-sig는 한글 인코딩을 위함
print(f"✅ 댓글이 '{SAVE_PATH}.csv' 파일로 저장되었습니다.")