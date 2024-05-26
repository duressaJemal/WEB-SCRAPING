from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

import pandas as pd
import time
import requests
import os


# Constants
WEB_URL = "https://jmapps.ne.jp/apmoa2/list.html?is_pub_mode=1&museum_sub_domain=apmoa2&kwd_and_or=and&title=&f3=&f6=&f9=&f7=&hlvl=1&bunrui=0&uni_museum=&keywords=&kwd_and_or=and&search_type=keyword&sort_type=asc&page=1&list_type=LLG&btn_list_type=yes&list_count=50"
SAVE_DIRECTORY = os.getcwd()

# Function to initialize the driver
def initialize_driver():
    # config
    options = Options()
    options.add_experimental_option("detach", True) # keep browser open after script ends

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

def main():

    # Initialize the driver
    driver = initialize_driver()
    session = save_session_cookies(driver)

    # Initialize variables
    image_url = []

    # Find the container and section
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//ul[@class='type-pict']")))
    section = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, "./li")))

    for i in section:
        # image = WebDriverWait(i, 5).until(EC.presence_of_all_elements_located((By.XPATH, "./dl/dt/img[not(contains(src, 'no_image'))]")))
        image = i.find_elements(By.XPATH, "./dl/dt/img[not(contains(@src, 'no_image'))]")
        if len(image) > 1:
            image = image[1]
        else:
            continue
        src = image.get_attribute("src")
        image_url.append(src)
        print("image source", src)

    # Download and save images
    for i, url in enumerate(image_url):
        filename = os.path.join(SAVE_DIRECTORY, f"image_{i}.png")
        download_image(url, filename, session)

if __name__ == "__main__":
    main()