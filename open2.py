import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import requests
from bs4 import BeautifulSoup
import googlemaps

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--incognito")

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.txdpsscheduler.com/")
    driver.maximize_window()

    #setting language
    lang_btn = driver.find_element(By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.container > button:nth-child(1)")
    lang_btn.click()

    #filling form and logging in
    first_name = driver.find_element(By.ID, "input-55")
    last_name = driver.find_element(By.ID, "input-58")
    dob = driver.find_element(By.ID, "dob")
    ssn = driver.find_element(By.ID, "last4Ssn")

    first_name.send_keys("Rachel Shirin")
    last_name.send_keys("Padibandla")
    dob.send_keys("09/27/1997")
    ssn.send_keys("1234")

    driver.implicitly_wait(60)
    login_btn = driver.find_element(By.CSS_SELECTOR, "#app > section > div > main > div > section > div.px-3 > div > div > form > div.menucard.form.mx-auto.mt-8.v-card.v-card--outlined.v-card--shaped.v-sheet.theme--light > div.v-card__actions.text-center > button")
    login_btn.click()

    #after login
    driver.implicitly_wait(40)
    new_apt_btn = driver.find_element(By.CSS_SELECTOR, "#app > section > div > main > div > section > div.px-3 > div > div > div.row.px-10.pt-2 > div > button")
    new_apt_btn.click()

    driver.implicitly_wait(20)
    pop_up_btn = driver.find_element(By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__actions.pt-0 > button")
    pop_up_btn.click()

    driver.implicitly_wait(20)
    apply_first_time_btn = driver.find_element(By.CSS_SELECTOR, "#app > section > div > main > div > section > div.px-3 > div > main > div > div > div:nth-child(1) > div:nth-child(2) > button")
    apply_first_time_btn.click()

    #filling data
    cell_phone = driver.find_element(By.CSS_SELECTOR, "#input-135")
    email = driver.find_element(By.CSS_SELECTOR, "#input-138")
    verify_email = driver.find_element(By.CSS_SELECTOR, "#input-141")

    cell_phone.send_keys("2145377592")
    email.send_keys("rachelshirin123@gmail.com")
    verify_email.send_keys("rachelshirin123@gmail.com")

    driver.find_element(By.CSS_SELECTOR, "#app > section > div > main > div > section > div.px-3 > div > form > div > div:nth-child(1) > div > div.layout.ml-5.mt-n4.row.wrap > div > div:nth-child(1) > div > div.v-input__slot > div > div").click()

    #selecting a place

    '''cities_to_search = {'Richardson': '#list-168', 'Dallas': '#list-992 > div:nth-child(1)', 'Plano': '#list-992 > div'}

    # Assign dictionary values to two variables
    for key, value in cities_to_search.items():
        # Now 'key' holds the key, and 'value' holds the value
        print(f"City: {key}, Selector_Value: {value}")'''


    city = driver.find_element(By.ID, "city")
    city.send_keys("Richardson")

    driver.implicitly_wait(20)
    list_btn = driver.find_element(By.CSS_SELECTOR, "#list-992 > div")
    list_btn.click()

    driver.implicitly_wait(20)
    next_btn = driver.find_element(By.CSS_SELECTOR, "#app > section > div > main > div > section > div.px-3 > div > form > div > div:nth-child(2) > div.row > div > div.flex.sm4.ml-3 > button")
    next_btn.click()

    #identify rows in table
    rows = 1+len(driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/main/div/div/section/div/main/div/section/div[2]/div/div[1]/div/table/tbody/tr'))
    print("num of rows = ", rows)
    cols = len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/main/div/div/section/div/main/div/section/div[2]/div/div[1]/div/table/tbody/tr/td[1]"))
    print("num of cols = ", cols)

    #print headers
    headers = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/main/div/div/section/div/main/div/section/div[2]/div/div[1]/div/table/thead")
    for i in headers:
        print(i.text)

    #print rows and cols
    r1 = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/main/div/div/section/div/main/div/section/div[2]/div/div[1]/div/table/tbody/tr")
    for j in r1:
        print(j.text)

    pd.set_option('display.max.columns', 7)
    pd.set_option('display.max.rows', 10)

    df = pd.read_html(driver.page_source)[0]
    print(df.head())

    df2 = pd.read_html(driver.page_source)[1]
    print(df2.head())

    print("--------------Here comes the main part----------------------------")
    #removing column 3 because it is not necessary
    column_numbers = [x for x in range(df2.shape[1])]  # list of columns' integer indices

    column_numbers.remove(3)  # removing column integer index 0
    df3 = df2.iloc[:, column_numbers]

    #doing outer join to merge them
    df = pd.merge(df, df3, how='outer', left_on=['businessSelected Location','Proximity','Next Available Date'], right_on=[0,1,2])

    print(df)

    #removing columns 0,1,2
    column_numbers = [x for x in range(df.shape[1])]  # list of columns' integer indices

    column_numbers.remove(3)  # removing column integer index 0
    column_numbers.remove(4)
    column_numbers.remove(5)
    df = df.iloc[:, column_numbers]
    print("-------------------after removing unnecessary columns---------------------------------")
    print(df)

    print("--------------------------Striping away in columns--------------------------------")
    df['Proximity'] = df['Proximity'].map(lambda x: x.lstrip('Proximity ').rstrip('(Map)'))
    df['Next Available Date'] = df['Next Available Date'].map(lambda x: x.lstrip('Next Available Date '))
    print(df)

    #writing into excel
    writer = pd.ExcelWriter('test5.xlsx', engine='openpyxl')  # Creating Excel Writer Object from Pandas
    df.to_excel(writer, sheet_name='Sheet1', index=False)  # Default position, cell A1.
    #df3.to_excel(writer, sheet_name='Sheet1', startrow=2, header=False, index=False)

    writer.close()

except KeyboardInterrupt:
    driver.quit()