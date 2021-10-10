import re
import datetime
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import requests


stock = pd.read_csv("./stock.csv")
target = stock.name

path = './chromedriver_ver_94.exe'
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

digikey_result.to_csv('./stock_crawling_' + str(datetime.date.today()) + '.csv', index_label='no')

driver.close()

class API:
  def __init__(self):
    pass

  def get_mouser(self, product_key):
    headers = {
      'accept': 'text/json',
      'Content-Type': 'text/json',
    }

    params = (
        ('apiKey', 'user-apiKey'),
    )

    data = '{"SearchByKeywordRequest": { "keyword": "' + str(product_key) + '", "records": 0, "startingRecord": 0, "searchOptions": "string", "searchWithYourSignUpLanguage": "string" }}'

    response = requests.post('https://api.mouser.com/api/v1.0/search/keyword', headers=headers, params=params, data=data)

    return int(re.sub('[^0-9]', '', response.json()['SearchResults']['Parts'][0]['Availability']))

API = API()
print(API.get_mouser('ZMOD4510AI1R'))
