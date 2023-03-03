import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
import pandas as pd

#read account from textfile
account = open('account.txt','r')
account = str(account.read()).split('\n')
# print(account)

#Chrome driver path as
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()

#Test ACME
login_page = 'https://acme-test.uipath.com/login'
update_page = 'https://acme-test.uipath.com/work-items/update/'
sha1_page = 'http://www.sha1-online.com/'
driver.get(login_page)

print('Open Acme with URL: '+login_page)
email_input = driver.find_element_by_id('email').send_keys(account[0])
pass_input = driver.find_element_by_id('password').send_keys(account[1])
press_login = driver.find_element_by_xpath('/html/body/div/div[2]/div/div/div/form/button').click()


check_dashboard = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="dashmenu"]/div[1]/button')))
print(driver.title)
print('Login successful')
workitem_enter = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,'//*[@id="dashmenu"]/div[2]/a/button')))
workitem_enter.click()
print(driver.title)

wi_type = list()
wi_id = list()
wi_des = list()
wi_status =list()
wi_comments = list()

#Check total page
get_count_pg = driver.find_elements_by_xpath("//ul[contains(@class,'page-numbers')]/li")
round_do = len(get_count_pg)-1
round_clk_next = round_do-1
# print(round_clk_next)
try:
    for i in range(round_do):
        cur_tb_rows = driver.find_elements_by_xpath("//table/tbody/tr")
        for ite_row in range(1,len(cur_tb_rows)):
            row_to_get_data = str(ite_row+1)

            # Get type
            td = driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr['+row_to_get_data+']/td[4]')
            tmp_td_txt = td.text
            
            # Get WIID
            wiid = driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr['+row_to_get_data+']/td[2]')
            tmp_id_txt = wiid.text

            # Get description
            des = driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr['+row_to_get_data+']/td[3]')
            tmp_des_txt = des.text

            # Get only type WI1
            if tmp_td_txt == 'WI4':
                #Append to lisy
                wi_type.append(tmp_td_txt)
                wi_id.append(tmp_id_txt)
                wi_des.append(tmp_des_txt)

                #Open sha1 URL following by WIID
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(sha1_page)

                sha_input = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.ID,"textToHashId")))
                sha_input.send_keys(tmp_id_txt)

                sha_clk_hash = driver.find_element_by_xpath('//*[@id="sha1-title"]/form/p[1]/input[2]')
                sha_clk_hash.submit()

                sha_result = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.ID,"result-sha1")))
                sha_to_paste = sha_result.text
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                wi_comments.append(sha_to_paste)

                #Open update URL following by WIID
                tmp_update_url = update_page+str(tmp_id_txt)
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(tmp_update_url)

                #Add comments
                text_area = WebDriverWait(driver,30).until(ec.element_to_be_clickable((By.ID, "newComment")))
                text_area.send_keys(str(sha_to_paste))

                #Chose type to 'Completed'
                select_type_to_update = Select(driver.find_element_by_id('newStatus'))
                select_type_to_update.select_by_value('Completed')

                #Click update
                click_update_comments = WebDriverWait(driver,30).until(ec.element_to_be_clickable((By.ID, "buttonUpdate")))
                click_update_comments.click()

                #Click ok alert
                time.sleep(5)
                alert_msg = driver.switch_to_alert().text
                # print(tmp_id_txt+': '+alert_msg)
                clk_ok = driver.switch_to_alert().accept()
                time.sleep(5)
                driver.close()

                #switch to get status
                driver.switch_to.window(driver.window_handles[0])
                driver.refresh()
                time.sleep(3)
                status_msg = driver.find_element_by_xpath('/html/body/div/div[2]/div/table/tbody/tr['+row_to_get_data+']/td[5]')
                tmp_status = status_msg.text
                wi_status.append(tmp_status)
                
            else:
                continue
        if i == round_clk_next:
            # Click logout
            clk_logout = driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[3]/a').click()
            time.sleep(3)
            print(driver.title)
            print('Logout - successful')
            # Create CSV
            data = pd.DataFrame([wi_id,wi_des,wi_type,wi_status,wi_comments]) #Each list would be added as a row
            data = data.transpose() #To Transpose and make each rows as columns
            data.columns=['WIID','Description','Type','Cur_status','Comments'] #Rename the columns
            data.to_csv('acme_test.csv')
        else:
            click_next = driver.find_element_by_link_text('>').click()
   
except:
    print('failed')
driver.quit()


