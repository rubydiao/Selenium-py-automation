import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
PATH = 'C:\Program Files (x86)\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")


driver = webdriver.Chrome(PATH,chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://www.rpachallenge.com/')
print(driver.title)

clk_start = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,"/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button")))
clk_start.click()
df = pd.read_excel('D:\Downloads\challenge.xlsx',dtype=str)
for i in range(len(df)):
    name = str(df.iloc[i,0])
    l_name = str(df.iloc[i,1])
    c_name = str(df.iloc[i,2])
    r_name = str(df.iloc[i,3])
    a_name = str(df.iloc[i,4])
    e_name = str(df.iloc[i,5])
    t_name = str(df.iloc[i,6])

    def input_element(name_variable,row):
        element = driver.find_element_by_xpath('/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div['+row+']/rpa1-field/div/input')
        # element.clear()
        element.send_keys(name_variable)
    for i in range(7):
        a = i+1
        input_1 = WebDriverWait(driver,5).until(ec.visibility_of_element_located((By.XPATH,"/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/div/div["+str(a)+"]"))).text
        if str(input_1) == 'First Name':
            input_element(name,str(a))
        elif str(input_1) == 'Last Name':
            input_element(l_name,str(a))
        elif str(input_1) == 'Email':
            input_element(e_name,str(a))
        elif str(input_1) == 'Address':
            input_element(a_name,str(a))
        elif str(input_1) == 'Role in Company':
            input_element(r_name,str(a))
        elif str(input_1) == 'Phone Number':
            input_element(t_name,str(a))
        elif str(input_1) == 'Company Name':
            input_element(c_name,str(a))
        else:
            continue
    submit_btn = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,'/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input')))
    submit_btn.click()
find_success = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,"/html/body/app-root/div[2]/app-rpa1/div/div[2]/div[1]"))).text
print(find_success)
find_time = WebDriverWait(driver,10).until(ec.visibility_of_element_located((By.XPATH,"/html/body/app-root/div[2]/app-rpa1/div/div[2]/div[2]"))).text
print(find_time)
driver.quit()
