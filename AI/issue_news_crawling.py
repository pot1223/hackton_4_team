from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# 네이버 뉴스 댓글 많이 섹션 진입 
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://news.naver.com/main/ranking/popularMemo.naver?date=20241026'
driver.get(url)

# 댓글 많이 섹션에 참여한 뉴스사 수 
rankingnews_list = len(driver.find_elements(By.XPATH, '//*[@id="wrap"]/div[4]/div[2]/div/div'))




# 뉴스사, 뉴스명, 뉴스내용, 뉴스날짜 수집
news = [] 
news_name = []
news_content = [] 
news_date = []

date_num = 1

while(date_num < 35):

    element_num = 0 
    for news_element in range(rankingnews_list):
        element_num += 1
        for content in range(1,6): 
            news.append(driver.find_element(By.XPATH,  f'//*[@id="wrap"]/div[4]/div[2]/div/div[{element_num}]/a/strong').text)
            time.sleep(2)
            driver.find_element(By.XPATH, f'//*[@id="wrap"]/div[4]/div[2]/div/div[{element_num}]/ul/li[{content}]/div/a').click()
            news_name.append(driver.find_element(By.XPATH,  f'//*[@id="title_area"]').text)
            news_date.append(driver.find_element(By.XPATH,  f'//*[@id="ct"]/div[1]/div[3]/div[1]/div[1]/span').text)
            news_content.append(driver.find_element(By.XPATH,  f'//*[@id="dic_area"]').text)
            driver.back()
            time.sleep(2)
    if date_num < 4 : 
        driver.find_element(By.XPATH,  f'//*[@id="wrap"]/div[4]/ul/li[{date_num+1}]/a').click()
        date_num += 1
        time.sleep(2)
    else: 
        driver.find_element(By.XPATH,  f'//*[@id="wrap"]/div[4]/ul/li[4]/a').click() 


# 수집한 데이터들을 데이터프레임으로 모음 
news_data = pd.DataFrame({"news" : news_2,"news_name" : news_name,"news_content" : news_content,"news_date" : news_date})

# 데이터프레임 내보냄
news_data.to_csv('news_data.csv', index=False, encoding='utf-8-sig')


