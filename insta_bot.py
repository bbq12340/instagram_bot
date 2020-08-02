#selenium package
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#time
import time
from datetime import datetime
#own
from workspace import (
    log_login, 
    log_post_info, 
    log_search_tags,
    log_followers_record,
    log_followers_list,
)


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
        admin = self.login(username, password)
        self.get_followers_list(admin)
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
            log_login(current_time)
            print(f"Safely logged in! TimeStamp: {current_time}")

            return self.browser
        except exceptions.NoSuchElementException:
            print("no such element")
            self.browser.close()
    def get_followers_list(self, admin):

        PROFILE_INFO = By.CLASS_NAME, "zwlfE"
        FOLLOWERS_XPATH = '//section[contains(@class="zwlfE")]/ul/li[2]'
        FOLLOWERS_CLASS_NAME = By.CLASS_NAME, "isgrP"
        FOLLOWERS_LIST = []

        self.browser.get(IG + self.username)
        self.wait.until(EC.presence_of_element_located(PROFILE_INFO))
        followers = self.browser.find_element_by_xpath(FOLLOWERS_XPATH)
        followers_count = int(followers.find_element_by_tag_name("span").get_attribute("innerText"))
        followers.click()
        self.wait.until(EC.presence_of_element_located(FOLLOWERS_CLASS_NAME))
        followers_list = self.browser.find_element_by_class_name('PZuss').find_elements_by_tag_name('li')

        #scroll until the count = len(list)
        followers_list_script = 'followerList = document.querySelector(".isgrP")'
        self.browser.execute_script(followers_list_script)
        while followers_count > len(followers_list):
            self.browser.execute_script('followerList.scrollTop = followerList.scrollHeight')
            followers_list = self.browser.find_element_by_class_name('PZuss').find_elements_by_tag_name('li')
            if followers_count == len(followers_list):
                for name in followers_list:
                    name = name.find_elements_by_class_name('FPmhX').get_attribute('innerText')
                    FOLLOWERS_LIST.append(name)
                now = datetime.now()
                log_followers_record(now, followers_count)
                log_followers_list(now, FOLLOWERS_LIST)
                break
        return 
    
    def locate_searchbar(self, browser):
        SEARCHBAR = "TqC_a"
        SEARCHBAR_EC = By.CLASS_NAME, SEARCHBAR
        try:
            query = browser.find_element_by_class_name(SEARCHBAR)
            return query
        except exceptions.NoSuchElementException:
            self.wait.until(EC.presence_of_element_located(SEARCHBAR_EC))

    def save_post_info(self, post_link):

        self.browser.get(post_link)
        time.sleep(3)

        POST_CONTENT_EC = By.CLASS_NAME, "QBXjJ"
        self.wait.until(EC.presence_of_element_located(POST_CONTENT_EC))

        USER_OTHER_POSTS = "Z666a"

        USER_ID = self.browser.find_element_by_class_name("sqdOP").get_attribute("innerHTML")
        QUOTES = self.browser.find_element_by_xpath('//div[contains(@class, "C4VMK")]/span').get_attribute('innerText')
        IMG= self.browser.find_elements_by_class_name("KL4Bh")
        
        try:
            other_posts = self.browser.find_element_by_class_name(USER_OTHER_POSTS)
            #delete user's other related posts
            for i in range(0,6):
                del IMG[-1]
            #get the src for every posted imgs
            for src in IMG:
                src = src.find_element_by_tag_name("img").get_attribute("src")
            post_IMG = IMG
        #skip del other related posts - "the element won't show since the user has less than 6 posts"
        except exceptions.NoSuchAttributeException:
            for src in IMG:
                src = src.find_element_by_tag_name("img").get_attribute("src")
            post_IMG = IMG
        POST_INFO = {
            "user": USER_ID,
            "quotes": QUOTES,
            "img": post_IMG,
        }

        return POST_INFO


    def search_by_tags(
        self, 
        TAGS: list,
        amount: int=5,
        only_recent: bool=False,
        ):

        EXPLORE_TAGS = By.CLASS_NAME, "drKGC"
        ARTICLE = By.CLASS_NAME, "KC1QD"
        self.only_recent = only_recent

        def count_posts(article):
            POSTS_LINK = []
            POSTS = article.find_elements_by_tag_name("a") #length=33
            for p in POSTS:
                p = str(p.get_attribute('href'))
                POSTS_LINK.append(p)
            return POSTS_LINK
    
        def log_post_info(POSTS_LINK):
            if self.only_recent == True:
                for i in range(0,9):
                    del POSTS_LINK[0]
                for i in range(0, amount):
                    post_info = self.save_post_info(POSTS_LINK[i])
                    log_post_info(post_info)
                    print(i, post_info)
            else:
                for i in range(0, amount):
                    post_info = self.save_post_info(POSTS_LINK[i])
                    log_post_info(post_info)
                    print(i, post_info)

        for tag in TAGS:
            #locates searchbar
            query = self.locate_searchbar(self.browser)
            query.click()
            PROGRESS_STRING = "searching #{tag} - {TAGS.index(tag)+1}/{len(TAGS)}"
            log_search_tags(PROGRESS_STRING)
            print(PROGRESS_STRING)
            selected_query = self.browser.find_element_by_class_name('XTCLo')
            selected_query.send_keys("#"+tag)
            self.wait.until(EC.presence_of_all_elements_located(EXPLORE_TAGS))
            selected_query.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
            self.wait.until(EC.presence_of_all_elements_located(ARTICLE))
            article = self.browser.find_element_by_class_name("KC1QD")
            POSTS_LINK = count_posts(article)
            #delete all the popular posts link
            time.sleep(1)
            while amount >= len(POSTS_LINK):
                current_height = "window.scrollY"
                max_height = "document.body.scrollHeight"
                self.browser.execute_script(f"window.scrollBy({current_height}, {max_height});")
                self.wait.until(EC.presence_of_all_elements_located(ARTICLE))
                POSTS_LINK = count_posts(article)
                time.sleep(5)
                if amount < len(POSTS_LINK):
                    log_post_info(POSTS_LINK)
                    break
            time.sleep(10)
        return self.browser






