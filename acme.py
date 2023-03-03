from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
import time
from datetime import timedelta
start_time = time.monotonic()

#Get config
config = open("config.txt","r")
config_list = list()
for iter_config in config:
    config_list.append(iter_config)

url_acme = config_list[0].split("=")[1].strip()
user_acme = config_list[1].split("=")[1].strip()
pwd_acme = config_list[2].split("=")[1].strip()
url_sha = config_list[3].split("=")[1].strip()

driver = webdriver.Firefox()
driver.get(url_acme)

try:
    #login Acme
    fill_email = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.ID,"email"))).send_keys(user_acme)
    fill_pwd = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.ID,"password"))).send_keys(pwd_acme)
    logon_btn = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"body > div > div.main-container > div > div > div > form > button"))).click()

    #Go to WorkItem
    workItem_btn = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.CSS_SELECTOR,"#dashmenu > div:nth-child(2) > a > button"))).click()

    #Scrapping WIID , status open
    go_next = True
    listWIID = list()
    while(go_next):
        header = WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.CLASS_NAME,"page-header"))).text
        # print(header)
        rowData = driver.find_elements(By.TAG_NAME,"tr")
    
        for ite_row in rowData:
            WIID = ite_row.find_elements(By.CSS_SELECTOR, "td:nth-child(2)")
            Status = ite_row.find_elements(By.CSS_SELECTOR, "td:nth-child(5)")
            wiType = ite_row.find_elements(By.CSS_SELECTOR, "td:nth-child(4)")
            for iter_data in range(len(WIID)):
                if(Status[iter_data].text == "Open" and wiType[iter_data].text == "WI3"):
                    listWIID.append(WIID[iter_data].text)
                else:
                    pass
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR,"body > div > div.main-container > div > nav > ul > li.page-item > a").click()
        except NoSuchElementException:
            go_next = False
            print("End Scrapping WIID")

    #Go Sha1 Page
    sha1_pg = driver.get(url_sha)
    result_gen = list()
    for iter_wiid in listWIID:
        #fill WIID
        fill_wiid_bar = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.ID,"textToHashId")))
        fill_wiid_bar.clear()
        fill_wiid_bar.send_keys(iter_wiid)

        #Click Hash and Get result
        hash_btn = driver.find_element(By.CSS_SELECTOR,"#sha1-title > form > p:nth-child(1) > input[type=submit]:nth-child(2)").click()
        hash_res = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.ID,"result-sha1"))).text
        print(hash_res)
        result_gen.append(hash_res)

    #UPDATE item
    for iter_res in range(len(result_gen)):
        update_pg = driver.get("https://acme-test.uipath.com/work-items/update/"+listWIID[iter_res].strip())
        fill_res = WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.ID,"newComment"))).send_keys(result_gen[iter_res])
        completed_btn = driver.execute_script("document.querySelector('#loginForm > div:nth-child(2) > div > div > div > ul > li:nth-child(4) > a').click()")
        update_btn = driver.find_element(By.ID,"buttonUpdate").click()
        wnd_alert = WebDriverWait(driver,10).until(ec.alert_is_present())
        alert_msg = wnd_alert.text
        print(alert_msg+" : "+listWIID[iter_res].strip())
        wnd_alert.accept()
except NoSuchElementException as ex:
    print(ex)
except TimeoutException as ex:
    print(ex)
except ElementNotVisibleException as ex:
    print(ex)
finally:
    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))
    driver.quit()
