import selenium
from selenium.webdriver.common.keys import Keys
import datetime
import re
import tqdm
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import random
import math
import requests
import pandas as pd
from selenium.common.exceptions import NoSuchElementException as NSEE


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않는 옵션
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')  # headless 옵션으로 서버에서 차단당하지 않기위해 넣는 옵션
# driver = webdriver.Chrome('C:/Users/brain/Desktop/crawling/code/chromedriver.exe', options=chrome_options) # 입력


driver = webdriver.Chrome('./chromedriver.exe')  # chrome driver 입력
driver.implicitly_wait(30)
_keyword = 'art' # 검색할 키워드
url = 'https://www.instagram.com/explore/tags/'+_keyword
# url = 'https://www.instagram.com/explore/tags/cat/'
driver.get(url)
driver.implicitly_wait(30)
time.sleep(4)

try:
    driver.find_element(By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
except:
    print("하..")

def login():  # 로그인
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').click()
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys('hihihisu1231')  # ID
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').click()
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys('h9e8e1s2o3o1')  # PWD
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    # pyautogui.click(472, 642)
    time.sleep(5)


#     pyautogui.click(487, 719)
#     time.sleep(5)


time.sleep(3)
login()
rep = []
#driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]').click()
driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click() #첫번째 게시물 열기
time.sleep(5)

all = []
count = 3  # 몇개의 게시물을 할건지
for i in tqdm.tqdm(range(count)):
    try:
        hashtags = []
        sources = []
        image_list = []
        # 해시태그
        # 이미지
        overlapphoto = driver.find_elements_by_class_name("Yi5aA")
        if (len(overlapphoto) == 0):
            try:
                image = driver.find_element_by_css_selector('div._97aPb.C2dOX   img.FFVAD')
                images = image.get_attribute('src')
                image_list.append(images)
            except:
                images = "error"
                print("이미지 저장 실패" + str(i))
        else:
            for n in range(len(overlapphoto)):
                try:
                    image = driver.find_element_by_css_selector('div._97aPb.C2dOX   img.FFVAD')
                    images = image.get_attribute('src')
                    image_list.append(images)
                except:
                    images = "error"
                    print("이미지 저장 실패" + str(i))
                try:
                    driver.find_element_by_class_name("coreSpriteRightChevron").click()
                except:
                    continue

        try:
            data = driver.find_elements_by_css_selector('a.xil3i')  # 해쉬태그 정보 저장
            for j in range(len(data)):
                hashtags.append(data[j].text.replace("#", ""))  # '#'없애기
            contents_html = driver.page_source
            contents_bs = BeautifulSoup(contents_html, 'lxml')
            contents = contents_bs.find('div', {'class', 'C4VMK'}).get_text()
        except:
            print("해시태그 저장 실패" + str(i))

        try:
            location_object = driver.find_element_by_css_selector("div.o-MQd.z8cbW > div.M30cS > div._7UhW9.PIoXz.MMzan.KV-D4.uL8Hv.T0kll > div.JF9hh > div._7UhW9.PIoXz.MMzan._0PwGv.fDxYl.T0kll > a.O4GlU")
            location_info = location_object.text
            location_href = location_object.get_attribute("href")
        except:
            location_info = None
            location_href = None
            print("장소 저장 실패" + str(i))

        try:
            upload_id_object = driver.find_element_by_css_selector("div.e1e1d > div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv.T0kll > span.Jv7Aj.mArmR.MqpiF  > a ")
            upload_id = upload_id_object.text
        except:
            upload_id = None
            print("id 저장 실패" + str(i))

        try:
            date_object = driver.find_element_by_css_selector("div.C7I1f.X7jCj > div.C4VMK > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.pjcA_.aGBdT > div._7UhW9.PIoXz.MMzan._0PwGv.uL8Hv > time.FH9sR.RhOlS")
            date_text = date_object.text
            date_time = date_object.get_attribute("datetime")
            date_title = date_object.get_attribute("title")
        except:
            date_text = None
            date_time = None
            date_title = None
            print('date 저장 실패' + str(i))



        all.append([hashtags, contents, image_list, location_info, location_href, date_text, date_time, date_title, upload_id])

        if (i + 1) % 10 == 0:
            print('{}번째 게시물 완료'.format(i + 1))
        next_arrow_btn = driver.find_element_by_css_selector("div.l8mY4.feth3 > .wpO6b ")  # 다음 게시물로 이동
        next_arrow_btn.send_keys(Keys.ENTER)

        time.sleep(3)

    except AttributeError:
        print("pass" + str(i))
        next_arrow_btn = driver.find_element_by_css_selector("div.l8mY4.feth3 > .wpO6b ")  # 다음 게시물로 이동
        next_arrow_btn.send_keys(Keys.ENTER)
        continue

image = driver.find_element_by_css_selector('div._97aPb.C2dOX   img.FFVAD')
image_url=image.get_attribute('src')
image_url

# next_arrow_btn = driver.find_element_by_css_selector("div.l8mY4.feth3 > .wpO6b ") #다음 게시물로 이동
# next_arrow_btn.send_keys(Keys.ENTER)

df = pd.DataFrame(all,columns=["hashtags","contents","images", "location_info", "location_href", "date_text", "date_time", "date_title", "upload_id"])

filename = datetime.datetime.now().strftime("%m월 %d일 %H시%M분")
df.to_csv('result/'+_keyword+filename+".csv", encoding='utf-8-sig')