from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def save_post_info(browser, post_link):
    wait = WebDriverWait(browser, 10)
    
    POST_CONTENT = browser.find_element_by_class_name("QBXjJ")
    USER_ID = browser.find_elements_by_class_name("sqdOP").get_attribute("innerHTML")
    QUOTES = browser.find_elements_by_class_name("C4VMK").find_elements_by_tag_name("span").get_attribute("innerHTML")

    POST_INFO = {
        "user": USER_ID,
        "quotes": QUOTES,
        
    }

    browser.get(post_link)
    wait.until(EC.presence_of_all_elements_located(POST_CONTENT)
