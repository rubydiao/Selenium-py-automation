import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

PATH = 'C:\Program Files (x86)\chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


driver = webdriver.Chrome(PATH,chrome_options=chrome_options)
driver.maximize_window()
driver.get('http://automationpractice.com/index.php')
# print(driver.title)
try:
    search_pro_duct = ['T-SHIRTS','DRESSES','BLOUSES']
    for product_to_search in search_pro_duct:
        h1_chk = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.ID,"search_query_top")))
        h1_chk.clear()
        h1_chk.send_keys(product_to_search)

        clk_btn = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="searchbox"]/button')))
        clk_btn.submit()

        try:
            chk_not_found = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="center_column"]/p')))
            text_keep = str(chk_not_found.text)
            if text_keep.startswith('No results were found') == True:
                print(text_keep)
                driver.quit()
            else:
                pass
        except:
            product = WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="center_column"]/ul/li/div/div[1]/div/a[1]')))
            amount_product = driver.find_element_by_xpath('//*[@id="center_column"]/h1/span[2]')
            count_pro = int(str(amount_product.text).split(' ')[0])

            def get_detail():
                product = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="center_column"]/div/div/div[3]/h1')))
                print('Product name is: '+product.text)
                product_price = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.ID,'our_price_display')))
                print('Product price is: '+product_price.text)
                conditon = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="product_condition"]/span')))
                print('Condition is: '+conditon.text)
                style_des = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="center_column"]/div/section[1]/table/tbody/tr[2]/td[2]')))
                print('Style :'+style_des.text)
                info_product = WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH,'//*[@id="center_column"]/div/section[2]/div/p')))
                print('Info : '+info_product.text)
                des_product = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,'#short_description_content')))
                print('Description : '+des_product.text)
                print('\n')

            if count_pro == 1:
                driver.execute_script('document.querySelector("#center_column > ul > li > div > div.left-block > div > a.product_img_link").click()')
                get_detail()
            else:
                for round_scrap in range(0,count_pro):
                    tmp_round = round_scrap+1
                    driver.execute_script('document.querySelector("#center_column > ul > li:nth-child('+str(tmp_round)+') > div > div.left-block > div > a.product_img_link").click()')
                    get_detail()
                    driver.back()
                    time.sleep(3)
except:
    print('Failed')
    driver.quit()
print('Search all product')
driver.quit()