from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
import pandas as pd
import random

def hasXpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def init_driver():
    chrome_path = "/Users/jordanliu/Desktop/Code/chromedriver"

    #chrome_path = r'C:\Users\Jordan\Desktop\chromedriver'
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--incognito')
    driver = webdriver.Chrome(chrome_path, options = chrome_options)
    return driver

driver = init_driver()
data = pd.DataFrame()
item_title_list = []
sku_list = []
price_list = []


# scrape for each page


counter = 0

driver.get('https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_0_boost_1')
WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="zg_browseRoot"]/ul/li[1]/a')))
time.sleep(3)
depart_count = 1
while hasXpath(driver,'//*[@id="zg_browseRoot"]/ul/li[' + str(depart_count) + ']/a'):
    driver.find_element_by_xpath('//*[@id="zg_browseRoot"]/ul/li[' + str(depart_count) + ']/a').click()
    depart_count += 1
    time.sleep(3)

    group_count = 1
    while hasXpath(driver, '//*[@id="zg_browseRoot"]/ul/ul/li[' + str(group_count) + ']/a'):
        driver.find_element_by_xpath('//*[@id="zg_browseRoot"]/ul/ul/li[' + str(group_count) + ']/a').click()
        time.sleep(3)
        group_count += 1

        cat_count = 1
        while hasXpath(driver, '//*[@id="zg_browseRoot"]/ul/ul/ul/li[' + str(cat_count) + ']/a'):
            driver.find_element_by_xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li[' + str(cat_count) + ']/a').click()
            time.sleep(3)
            cat_count += 1

            while True:


                badge_link = driver.find_elements_by_xpath('//span[@class="zg-badge-text"]')
                badge_num = len(badge_link)

                for item_num in range(1, badge_num + 1):

                    price_boo = True
                    if hasXpath(driver, '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/div[2]/a/span/span'):
                        price_xpath = '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/div[2]/a/span/span'
                        price = driver.find_element_by_xpath(price_xpath).text[1:]
                        price_list.append(price)
                    elif hasXpath(driver, '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/div/a/span/span'):
                        price_xpath = '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/div/a/span/span'
                        price = driver.find_element_by_xpath(price_xpath).text[1:]
                        price_list.append(price)
                    else:
                        price_boo = False

                    if hasXpath(driver, '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/a/div') and price_boo == True:
                        item_title_xpath = '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/a/div'
                        item_title = driver.find_element_by_xpath(item_title_xpath).text
                        item_title_list.append(item_title)

                        sku_xpath = '//*[@id="zg-ordered-list"]/li[' + str(item_num) + ']/span/div/span/a'
                        sku = driver.find_element_by_xpath(sku_xpath).get_attribute('href').split('/dp/')[1][:10]
                        sku_list.append(sku)

                print('sku ', len(sku_list))
                print('price', len(price_list))

                if hasXpath(driver, '//*[@id="zg-center-div"]/div[2]/div/ul/li[4]/a'):
                    driver.find_element_by_xpath('//*[@id="zg-center-div"]/div[2]/div/ul/li[4]/a').click()
                    time.sleep(3)
                else:
                    break

        else:
            driver.find_element_by_xpath('//*[@id="zg_browseRoot"]/ul/li/a').click()
            time.sleep(3)
    else:
        driver.find_element_by_xpath('//*[@id="zg_browseRoot"]/li/a').click()
        time.sleep(3)


data.insert(0, 'SKU', sku_list)
data.insert(1, 'Item Title', item_title_list)
data.insert(2, 'Amazon Price', price_list)


driver.close()
writer = pd.ExcelWriter('/Users/jordanliu/Desktop/google_drive/amazon/min_quant/AmazonTopSellerB', engine = 'xlsxwriter')
data.to_excel(writer)
writer.save()