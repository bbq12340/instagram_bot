from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

IG = "https://www.instagram.com/"

class Instabot:
    def __init__(
        self,
        username,
        password,
        headless_browser: bool=False,
    ):
        self.set_browser(IG)
        self.wait = WebDriverWait(self.browser, 10)
        self.username = username
        self.password = password
        self.logged_in_browser = self.login(username, password)
        time.sleep(10)
        self.located_searchbar = self.locate_searchbar(self.browser)
        self.search_by_tags(self.locate_searchbar)

    def set_browser(self, link):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        return self.browser.get(IG)

    def login(self, username, password):
        LOGIN_FORM = By.CLASS_NAME, "HmktE"
        self.wait.until(EC.presence_of_element_located(LOGIN_FORM))

        try:
            self.browser.find_element_by_name("username").send_keys('bbq12340@hotmail.com')
            self.browser.find_element_by_name("password").send_keys('davidj171', Keys.RETURN)
            return self.browser
        except exceptions.NoSuchElementException:
            print("no such element")
            self.browser.close()
    
    def locate_searchbar(self, browser):
        SEARCHBAR = By.CLASS_NAME, "XTCLo x3qfX"
        SEARCHBAR_XPATH = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div/div/span[2]'
        try:
            query = browser.find_element(By.XPATH, SEARCHBAR_XPATH)
            return query
        except exceptions.NoSuchElementException:
            self.wait.until(EC.presence_of_element_located(SEARCHBAR))

    def search_by_tags(self, query):
        TAGS = ['programming', 'coding']
        FOLLWING = []
        for tag in TAGS:
            query.click()
            print(f"searching {TAGS.index(tag)+1}/{len(TAGS)}")
            query.send_keys("#"+tag, Keys.RETURN)
            time.sleep(10)
            num = self.browser.find_elements_by_class_name('g47SY ')
            FOLLWING.append(num)
        print(FOLLWING)
        return FOLLWING
        


