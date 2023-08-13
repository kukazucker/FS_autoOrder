# import required libraries
import shutil
import time
import os

# import necessary functions
from browser import get_driver
from browser import prepare_window 
from actions import collect_order
from actions import save_screenshot
from actions import verification_form
from actions import confirm_order

def main():

    ### DELETE ALL COOKIES ###
    if os.path.isdir('User'):
        shutil.rmtree('User')

    ### THE SCREENSHOT AND COLLECTING THE ORDER ###
    driver = get_driver(True)
    time.sleep(1)
    # prepare the browser for order collection
    prepare_window(driver)
    time.sleep(1)
    # сабрать заказ
    collect_order(driver)
    # save screenshot of the order
    save_screenshot(driver)
    driver.quit()

    ### VERIFICATION STAGE ###
    driver = get_driver(False)
    # passing verification
    verification_form(driver)
    driver.quit()

    ### ORDER AND (OR) DELIVERY CONFIRMATION ###
    driver = get_driver(True)
    # order confirmation
    confirm_order(driver)
    driver.quit()



if __name__ == '__main__':
    main()
