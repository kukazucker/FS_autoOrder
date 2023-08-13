from selenium.webdriver.common.by import By
import time


# get inforamtion from user
def get_data(data):
    
    match data:

        case 'order':
            # what the user ordered
            order = [
                     {
                        'Name': 'Пицца 4 СЕЗОНА', 
                        'Amount': 2, 
                        'Option': '40 см.', 
                        'Сырный соус': 1, 
                        'Барбекю': 3
                     }, 
                     {
                        'Name': 'Темаки', 
                        'Amount': 1, 
                        'Option': 'Темаки с лососем'
                     },
                     {
                        'Name': 'Белла ди Маре', 
                        'Amount': 1, 
                        'Option': None,
                        'Фарфалле': 1
                     },  
                     {
                        'Name': 'Кофе Американо', 
                        'Amount': 4, 
                        'Option': None
                     },
                     {
                        'Name': 'Манако', 
                        'Amount': 1, 
                        'Option': None
                     }
                    ]
            return order
        
        case 'phone_number':
            # the user specifies his phone number
            phone_number = input("Введите свой номер: +7 ")
            # the user specifies how he wants to pass verification
            veri_method = input("Выберите способ авторизации (0 - телефон или 1 - telegram): ")
            return phone_number, veri_method
        
        case 'verification_code':
            # the user writes the verification code
            veri_code = input("Введите код верификации: ")
            return veri_code
        
        case _:
            # checking for an error in the request
            return "UNDEFINED CATEGORY!"


def regForm_inputs(driver):
    name = 'Пользователь Пользователь'
    # name
    driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div[1]/input").send_keys(name)
    # date
    bd = driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div[2]/div/div/div/div/input").click()
    time.sleep(0.3)
    bd = driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div[2]/div/div/div[2]/div/ul[2]/li[3]").click()
    # sex
    driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div[3]/div[1]/input").click()
    driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/div/div[3]/div[2]/div/div[1]/div[2]/div/div/div/ul/li[1]/div").click()
    # press 'Register' button
    driver.find_element(By.XPATH, "//*[@id='topBar']/div/div/div[2]/div/div/div[2]/form/button").click()

