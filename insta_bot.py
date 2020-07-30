from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from datetime import datetime



IG = "https://www.instagram.com/"

class Instabot:
    def __init__(
        self,
        username,
        password,
        headless_browser: bool=False,
    ):
        #set_browser
        self.set_browser(IG)
        self.wait = WebDriverWait(self.browser, 10)

        #insta_login
        self.username = username
        self.password = password
        self.logged_in_browser = self.login(username, password)
        time.sleep(10)

        #locate_searchbar


        #set_like_by_tags



    def set_browser(self, link):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.set_window_position(0,0)
        self.browser.set_window_size(600, 800)
        return self.browser.get(IG)

    def login(self, username, password):
        LOGIN_FORM = By.CLASS_NAME, "HmktE"
        self.wait.until(EC.presence_of_element_located(LOGIN_FORM))

        try:
            self.browser.find_element_by_name("username").send_keys('bbq12340@hotmail.com')
            self.browser.find_element_by_name("password").send_keys('davidj171', Keys.RETURN)

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f"Safely logged in! TimeStamp: {current_time}")

            return self.browser
        except exceptions.NoSuchElementException:
            print("no such element")
            self.browser.close()
    
    def locate_searchbar(self, browser):
        SEARCHBAR = "TqC_a"
        SEARCHBAR_EC = By.CLASS_NAME, SEARCHBAR
        try:
            query = browser.find_element_by_class_name(SEARCHBAR)
            return query
        except exceptions.NoSuchElementException:
            self.wait.until(EC.presence_of_element_located(SEARCHBAR_EC))


    def set_like_by_tags(
        self, 
        TAGS: list,
        amount: int=5,
        only_recent: bool=False,
        ):

        EXPLORE_TAGS = By.CLASS_NAME, "drKGC"
        ARTICLE = By.CLASS_NAME, "KC1QD"
        POSTS = []

        for tag in TAGS:
            #locates searchbar
            query = self.locate_searchbar(self.browser)
            query.click()
            print(f"searching #{tag} - {TAGS.index(tag)+1}/{len(TAGS)}")
            selected_query = self.browser.find_element_by_class_name('XTCLo')
            selected_query.send_keys("#"+tag)
            self.wait.until(EC.presence_of_all_elements_located(EXPLORE_TAGS))
            selected_query.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
            self.wait.until(EC.presence_of_all_elements_located(ARTICLE))
            article = self.browser.find_element_by_class_name("KC1QD")
            POSTS = article.find_elements_by_tag_name("a")
            #delete all the popular posts link
            if only_recent == True:
                for i in range(0,9):
                    del POSTS[0]
                for link in range(0, amount):
                    post_link = POSTS[link].get_attribute('href')
            else:
                for link in range(0, amount):
                    print(POSTS[link].get_attribute('href'))
            time.sleep(10)
        return self.browser






