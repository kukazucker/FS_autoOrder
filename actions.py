from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import os

from browser import element_is_active
from data import get_data
from data import regForm_inputs
from browser import is_night

def collect_order(driver):
    # get an order
    order = get_data('order')
    # select all positions of meals on the website
    all_meals = driver.find_elements(By.CLASS_NAME, "product")
    last_meal = ''

    for meal in order:
        # every dish from all the products on the site
        for meal_position in all_meals:

            meal_heading = meal[list(meal.keys())[0]]
            # if the name of the dish matches the dish from the order, and also should not be repeated
            if meal_heading == meal_position.find_element(By.CLASS_NAME, 'heading').text and meal_heading != last_meal:
                last_meal = meal_heading
                # find a photo of a position
                photo_meal = meal_position.find_element(By.CLASS_NAME, 'heading')
                driver.execute_script("arguments[0].click();", photo_meal)
                time.sleep(1)
                # add the dish how many times in the request
                for i in range(meal[list(meal.keys())[1]] - 1):
                    # click on the add button
                    plus = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/div[2]/div[2]/div[2]/button[2]')
                    driver.execute_script("arguments[0].click();", plus)

                # check if the dish has an option
                extra_option = meal[list(meal.keys())[2]]
                # check if the dish has any modifiers
                all_modifiers = list(meal.keys())[3:]

                # if so
                if extra_option != None:
                    # then click on the option selection
                    opt_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div/button')
                    driver.execute_script("arguments[0].click();", opt_btn)
                    time.sleep(1)
                    # finding all the options
                    options = driver.find_elements(By.CLASS_NAME, 'options__item')
                    # we check them for compliance
                    for option in options:
                        if option.text == extra_option:
                            driver.execute_script("arguments[0].click();", option)

                # if modifiers are present
                if len(all_modifiers) > 0:
                    
                    for mod_option in all_modifiers:
                        # find all modifiers
                        modifiers = driver.find_elements(By.CLASS_NAME, 'modifier-item__wrapper')
                        for modifier in modifiers:
                            # if the modifier is found among the lists
                            if mod_option == modifier.find_element(By.CLASS_NAME, 'modifier-item__name').text:
                                for i in range(meal[mod_option]):
                                    
                                    if i == 0:
                                        driver.execute_script("arguments[0].click();", modifier)
                                    else:
                                        btn = modifier.find_element(By.CLASS_NAME, 'button')
                                        driver.execute_script("arguments[0].click();", btn)
                                    
        print(f'Блюдо: {last_meal} добавлено в заказ!')
        # click on the order confirmation button
        confirm_btn = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/div[2]/button')
        driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
        driver.execute_script("arguments[0].click();", confirm_btn)
        # wait for the window to close
        time.sleep(1)
        
    # notify about order collection
    print('ЗАКАЗ СОБРАН!')

def save_screenshot(driver):

    time.sleep(2)
    # click on the shopping cart
    price_btn = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[1]/button")
    driver.execute_script("arguments[0].click();", price_btn)
    # find the shopping cart window with the entire order
    ff = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[2]/div/div[1]/div")
    # expand the window to be able to photograph an order with more than 5 positions.
    driver.execute_script("arguments[0].setAttribute('style', 'max-height: 2500px')", ff)
    # wait for the blur effect to disappear at the window
    time.sleep(2)

    # time and date to save the screenshot
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    current_date = now.today().strftime('%Y-%m-%d')
    # folder for each new day
    date_path = './date_{}/sample.txt'.format(current_date)
    # if the folder for today does not exist
    if not os.path.exists(os.path.dirname(date_path)):
        # create a new folder
        os.makedirs(os.path.dirname(date_path))

    # save screenshot
    time.sleep(1)
    user_path = os.getcwd()
    # driver.find_element(By.CLASS_NAME, "popover__content").screenshot('{}/date_{}/order-{}.png'.format(user_path, current_date, current_time))
    driver.find_element(By.CLASS_NAME, "popover__content").screenshot('{}/date_{}/order_{}.png'.format(user_path, current_date, current_time))

    print('СНИМОК ЭКРАНА СОХРАНЁН!')


def verification_method(driver, veri_method, phone_number):
    
    # input phone number
    driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div[1]/div[1]/input").send_keys(phone_number)
    # depending on the verification method, click on
    if int(veri_method) == 0:
        'Телефон'
        driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div[2]/div/button[1]").click()
    else:
        'Telegram'
        driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div[2]/div/button[2]").click()
        # wait for the telegram link generation to finish
        element_is_active(driver, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div[2]/div/button[2]", 'telegram_token')
        print("ПОЖАЛУЙТСА, ПРОЙДИТЕ ВЕРИФИКАЦИЮ ПО ССЫЛКЕ: ", driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/div/a").get_attribute('href'))
        # wait for the end of receiving the link to the bot
        element_is_active(driver, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]", 'registration')
        # wait for the end of authentication via the bot
        element_is_active(driver, "/html/body/div[4]/div[2]/iframe", 'captcha')

    time.sleep(1)

def verification_form(driver):

    time.sleep(3)
    # does the customer order at night
    is_night(driver)
    # get the user's number and verification method
    phone_number, veri_method = get_data('phone_number')

    # click on the profile button
    driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div/button").click()
    # click on the verification button
    verification_method(driver, veri_method, phone_number)
    time.sleep(2)
    # wait until the captcha is passed
    element_is_active(driver, "/html/body/div[4]/div[2]/iframe", 'captcha')

    try:
        # click on the verification button again if the button was not pressed automatically
        driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div[2]/div/button[1]").click()
    except:
        pass

    # if the answer is no, then insert the number and wait for confirmation, if not, then run the full cycle
    new_user = input("Вы зарегестрированный пользователь? (0 - нет, 1 - да): ")
    # if the user is not registered
    if int(new_user) == 0:
        time.sleep(3)
        # close the warning window
        driver.find_element(By.CLASS_NAME, "close").click()
        # wait for the form to be loaded
        time.sleep(3)
        # we enter the user's data and click on the check
        regForm_inputs(driver)

    # request verification code
    verification_code = get_data('verification_code')
    # verification code field
    element_locator = driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div/input")
    time.sleep(1)
    # input the verification code
    element_locator.send_keys(verification_code)
    # while the registration is being confirmed
    print("ЕСЛИ ВЫ УВИДИТЕ, ЧТО САЙТ ЗАПРАШИВАЕТ КОД ПОВТОРНО: НАЖМИТЕ НА КНОПКУ 'ПОЛУЧИТЬ КОД В СМС' И ВВЕДИТЕ КОД САМОСТОЯТЕЛЬНО В ОКНО!")
    element_is_active(driver, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div/input", 'registration')

    time.sleep(1)

def preorder(driver):
    
    if datetime.today().hour > 22 or datetime.today().hour < 10:
        # click preorder button
        preorder_btn = driver.find_element(By.XPATH, "//*[@id='app']/main/div[2]/form/div/div/div[1]/div[2]/ul/li[1]/div/label/span")
        driver.execute_script("arguments[0].click();", preorder_btn)
        # clikc calendar button
        date_btn = driver.find_element(By.XPATH, "//*[@id='app']/main/div[2]/form/div/div/div[1]/div[2]/ul/li[2]/div/div/div/div")
        driver.execute_script("arguments[0].click();", date_btn)
        # find checkout window
        checkout = driver.find_element(By.XPATH, "//*[@id='app']/main/div[2]/form/div/div/div[1]/div[2]")
        # find calendar and all days in the checkout window
        calendar = checkout.find_element(By.CLASS_NAME, "popover__content")
        days_btns = calendar.find_elements(By.CLASS_NAME, "date-days__item")
        # check for every day
        for day_btn in days_btns[1:]:
            # if this day is tomorrow
            if int(day_btn.text) == int(datetime.today().day)+1:
                # then click the button
                driver.execute_script("arguments[0].click();", day_btn)    
                print('Вы сможете забрать заказ {} числа'.format(day_btn.text))


def confirm_order(driver):

    time.sleep(1)
    # does the user order at night
    is_night(driver)

    # click on the shopping cart
    btn = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div/button")
    driver.execute_script("arguments[0].click();", btn)
    # press 'place the order' button
    btn = driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/div[2]/div/button")
    driver.execute_script("arguments[0].click();", btn)

    time.sleep(3)
    # wait for the end of the captcha passage, if necessary
    element_is_active(driver, '/html/body/div[4]/div[2]/iframe', 'captcha')

    # press 'payment method' button
    elem = driver.find_element(By.XPATH, "//*[@id='app']/main/div[2]/form/div/div/div[1]/div[2]/ul/li[4]/div/div/input")
    ActionChains(driver).move_to_element(elem).click().perform()
    # choose 'By card to the courier'
    payment_choose_btn = driver.find_element(By.XPATH, "//*[@id='app']/main/div[2]/form/div/div/div[1]/div[2]/ul/li[4]/div/div[2]/div/div[1]/div[2]/div/div/div/ul/li[1]/div")
    driver.execute_script("arguments[0].click();", payment_choose_btn)
    time.sleep(1)
    # make a pre-order if necessary
    preorder(driver)

    # press 'order'
    order_btn = driver.find_element(By.XPATH, "//*[@id='app']/main/div[2]/form/div/div/div[1]/button")
    driver.execute_script("arguments[0].click();", order_btn)
    # wait until the order window disappears
    element_is_active(driver, "//*[@id='app']/main/div[2]/form/div/div/div[1]/button")
    print('ЗАКАЗ ПОДТВЕРЖДЁН!')

    time.sleep(3)
    # finish the script
    print('КОНЕЦ ТЕСТА!')