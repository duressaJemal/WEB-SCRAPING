from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


import pandas as pd
import time

# config
options = Options()
# head less mode is not working
# options.add_argument('--headless')
# # options.add_argument("--window-size=1920,1200")
options.add_experimental_option("detach", True) # keep browser open after script ends


web = "https://www.audible.com/adblbestsellers"
driver = webdriver.Chrome(options=options)
driver.get(web)
driver.maximize_window()

book_title, book_author, book_runtime = [], [], []

pagination = driver.find_element(By.XPATH, "//ul[contains(@class, 'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, "li")

last_page = pages[-2].text
current_page = 1

while current_page <= int(last_page):

    ## implicit wait: Better for testing purposes
    # time.sleep(3)

    ## explicit wait: Better for production

    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "adbl-impression-container")))
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, "./div/span/ul/li")))

    # container = driver.find_element(By.CLASS_NAME, "adbl-impression-container")
    # products = container.find_elements(By.XPATH, "./div/span/ul/li")

    for product in products:
        title = product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text
        # print("Title: ", title)
        book_title.append(title)
        book_author.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_runtime.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)

    current_page = current_page + 1 # increment page number

    try:
        next_page = driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]") # click the next page button
        next_page.click()
    except:
        pass


df = pd.DataFrame({"book_title": book_title, "book_author": book_author, "book_runtime": book_runtime})
df.to_csv("audible_books.csv", index=False)
print(df)
