from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import os

def get_driver(headless=False):
    # create webdriver
    options = webdriver.ChromeOptions()
    user_path = os.getcwd()
    options.add_argument(f'user-data-dir={user_path}/User')
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # headless mode
    if headless == True:
        options.add_argument("--headless=new") 
    
    driver = webdriver.Chrome(options=options)
    # set window size
    if headless == True:
        driver.set_window_size(2000, 8000)
    else:
        driver.set_window_size(800, 1000)
    # get url
    driver.get('https://shop.foodsoul.pro') 

    return driver

def is_night(driver):

    try:
        time.sleep(1)
        # is there a window with a warning about the impossibility of delivery
        modal = driver.find_element(By.CLASS_NAME, 'modal-card')
        modal.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/button[2]').click()

    except:
        pass

def prepare_window(driver):

    print('НАЧАЛО ТЕСТА!')
    
    time.sleep(1)

    # select and click on the 'pickup' button
    deli = driver.find_elements(By.CLASS_NAME, 'delivery-method__item')[1]
    driver.execute_script("arguments[0].click();", deli)

    # select and click on the button of the first store
    close = driver.find_elements(By.CLASS_NAME, 'pickup-item')[0]
    driver.execute_script("arguments[0].click();", close)   

    # skip the notification about the impossibility of delivery
    is_night(driver)
    
    # click on language button
    elem = driver.find_elements(By.CLASS_NAME,"topbar-item__name")[1]
    driver.execute_script("arguments[0].click();", elem)  
    time.sleep(1)
    # find button 'rus' and click
    rus_lang = driver.find_elements(By.CLASS_NAME, 'locales__item')[2]
    driver.execute_script("arguments[0].click();", rus_lang)   
    time.sleep(1)

    print('ЗАКАЗ ФОРМИРУЕТСЯ...')

def element_is_active(driver, elem, text=False):

    try:

        elem = driver.find_element(By.XPATH,"{}".format(elem))

        if text != False:
            match(text):
                case 'captcha':
                    print('Завершите прохождение капчи!')
                case 'registration':
                    print('Дождитесь окночания регистрации!')
                case 'telegram_token':
                    print('Дождитесь получения ссылки на телеграм бота!')
                case _:
                    print(text)

        while elem.is_displayed():
            time.sleep(0.1)

    except:
        pass
