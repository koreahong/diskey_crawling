import re
import datetime
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests


stock = pd.read_csv("C:/Users/korea/OneDrive/바탕 화면/exefile/stock.csv")
target = stock.name

path = 'C:/Users/korea/OneDrive/바탕 화면/exefile/chromedriver.exe'
driver = webdriver.Chrome(path)

digikey_result = []

driver.get("https://www.digikey.kr/")
wait = WebDriverWait(driver, 5)

for product_name in target:
    search_path = '//*[@id="header"]/div[1]/div[1]/div/div[2]/div[2]/input'
    element = wait.until(EC.visibility_of_element_located((By.XPATH, search_path)))
    element.send_keys(product_name)  #검색어입력하게 하는 부분
    element.send_keys("\n")  #엔터효과

    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productTable"]')))
        response = requests.get(url=driver.current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = soup.find_all('span', {'class': 'phone'})
        digikey_result.append([product_name, ", ".join(list(re.sub('[\r\n ]', '', price.text).split(':')[1] for price in prices))])
    except:
        try:
            product_stock_xpath = '//*[@id="dkQty"]'
            stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_stock_xpath)))
            digikey_result.append([product_name, stock_element.text])
        except:
            try:
                display_found_xpath = '//*[@id="exactPartList"]/table/tbody/tr/td[2]/span[1]/a'
                element = wait.until(EC.visibility_of_element_located((By.XPATH, display_found_xpath)))
                element.click()
                try:
                    product_stock_xpath = '//*[@id="dkQty"]'
                    stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_stock_xpath)))
                    digikey_result.append([product_name, stock_element.text])
                except:
                    product_nostock_xpath = '//*[@id="requestStockLinkButton"]'
                    stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_nostock_xpath)))
                    digikey_result.append([product_name, 0])
            except:
                digikey_result.append([product_name, '이름이 잘못됬거나 검색이 안됨'])

digikey_result = pd.DataFrame(digikey_result, columns=['name', 'digikey_stock'])

digikey_result.to_csv('./stock_crawling_' + str(datetime.date.today()) + '.csv')
driver.close()


### 마우저 검색
#
# mouser_result = []
#
# driver.get("https://kr.mouser.com/")
# wait = WebDriverWait(driver, 5)
# time.sleep(10)
#
# for product_name in target:
#     search_path = '/html/body/header/div[4]/div/div/div[2]/div/form/div/div/div[1]/div[1]/div[2]/input[1]'
#     element = wait.until(EC.visibility_of_element_located((By.XPATH, search_path)))
#     element.send_keys(product_name)  #검색어입력하게 하는 부분
#     element.send_keys("\n")  #엔터효과
#
#
#     ### 한번에 검색되는 경우
#     try:
#         product_stock_xpath = '//*[@id="pdpPricingAvailability"]/div[1]/h2"]'
#         stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_stock_xpath)))
#         mouser_result.append([product_name, re.sub('[^0-9]','', stock_element.text)])
#     except:
#         ### 검색이 안되는 경우
#         try:
#             alert_xpath = '/html/body/main/div/div/div[1]/div[3]'
#             stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, alert_xpath)))
#             mouser_result.append([product_name, '이름이 잘못됬거나 검색이 안됨'])
#         except:
#             ### 회사 이름이 나오는 경우
#             try:
#                 display_found_xpath = '//*[@id="leafCat_1"]'
#                 element = wait.until(EC.visibility_of_element_located((By.XPATH, display_found_xpath)))
#                 element.click()
#             except:
#                 pass
#
#             ### 상품이 검색되는 경우우
#             try:
#                 click_product_xpath = '//*[@id="lnkMfrPartNumber_1"]'
#                 element = wait.until(EC.visibility_of_element_located((By.XPATH, click_product_xpath)))
#                 element.click()
#             except:
#                 pass
#
#             ### 재고가 있는 경우
#             try:
#                 product_stock_xpath = '//*[@id="pdpPricingAvailability"]/div[1]/h2"]'
#                 stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_stock_xpath)))
#                 mouser_result.append([product_name, re.sub('[^0-9]', '', stock_element.text)])
#
#             ### 재고가 없는 경우
#             except:
#                 product_stock_xpath = '//*[@id="InStockNotify"]'
#                 stock_element = wait.until(EC.visibility_of_element_located((By.XPATH, product_stock_xpath)))
#                 mouser_result.append([product_name, 0])
#
#
#
# mouser_result = pd.DataFrame(mouser_result, columns=['name', 'mouser_stock'])