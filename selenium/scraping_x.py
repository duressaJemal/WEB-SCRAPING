from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

from fake_useragent import UserAgent
from dotenv import load_dotenv

import pandas as pd
import time
import requests
import os


load_dotenv()
# Constants
WEB_URL = "https://twitter.com/"
SAVE_DIRECTORY = os.getcwd()

# Function to initialize the driver
def initialize_driver():
    # config
    options = Options()

    # user agent
    ua = UserAgent()
    user_agent = ua.random

    options.add_experimental_option("detach", True)
    options.add_argument(f'user-agent={user_agent}')

    web = WEB_URL
    driver = webdriver.Chrome(options=options)
    driver.get(web)
    driver.maximize_window()

    return driver

# Function to save session cookies
def save_session_cookies(driver):
    cookies = driver.get_cookies()
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    return session

# Function to download and save an image
def download_image(url, filename, session):
    response = session.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
        print(f"Image downloaded and saved: {filename}")

def login_twitter(driver):

    time.sleep(4) # cancel the pop up welcome to twitter.

    login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/login"]')))
    login.click()

    # input username
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
    username.send_keys(os.getenv("TWITTER_USERNAME"))

    time.sleep(3)

    # find next button
    next_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button/div/span/span[contains(text(), 'Next')]")))
    next_button.click()

    # input password
    password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@name, 'password')]")))
    password.send_keys(os.getenv("TWITTER_PASSWORD"))

    time.sleep(2),

    # login
    login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']")))
    login.click()
    time.sleep(1)


def main():

    # Initialize the driver
    driver = initialize_driver()
    login_twitter(driver)

    # Initialize variables
    image_url = []


if __name__ == "__main__":
    main()