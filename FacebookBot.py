from secrets_1 import username,password
import requests, re, time, os
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class FacebookBot():
    session = None
    driver = None
    login_page = "https://www.facebook.com/login"
    payload = {
        'email': username,
        'pass': password
    }

    def __init__(self):
        # Initialize Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get("https://www.facebook.com")

        # Login to Facebook
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys(username)
        password_input = self.driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Allow some time for the page to load

        BASEURL = "https://www.facebook.com/groups/LeedsStudentsGroup"

        self.driver.get(BASEURL)
        time.sleep(5)


    def sendNotification(self, title, message):
        script = f'display notification "{message}" with title "{title}"'
        os.system(f"osascript -e '{script}'")


    #Open the posts file, if a new post exists that did not previously, 
    #add it to the file.
    def saveResults(self, foundPosts):
        with open("posts.txt", "r") as file:
            savedPosts = [line.strip() for line in file.readlines()]
        for post in foundPosts:
            if post not in savedPosts:
                self.sendNotification("New Post Found", post)
                with open("posts.txt", "a") as file:
                    file.write(post + "\n")
        

    def startScraping(self):
        actions = ActionChains(self.driver)
        for _ in range(randint(10,15)):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        foundPosts = []
        for post in soup.find_all("div", {"class" : "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"}):
            text = post.get_text().lower()
            if "leeds" in text and "ball" in text:
                foundPosts.append(post.get_text())

        self.saveResults(foundPosts)
        

        time.sleep(randint(300,900))
        self.driver.refresh()
        


def main():
    bot = FacebookBot()
    try:
        while True:
            bot.startScraping()
    except KeyboardInterrupt:
        print("Quitting bot")
    finally:
        bot.driver.quit()

    


if __name__ == "__main__":
    main()


    