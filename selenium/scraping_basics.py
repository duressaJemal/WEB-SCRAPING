from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

import pandas as pd
import time


# config
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) # keep browser open after script ends

website = "https://www.adamchoi.co.uk/overs/detailed"
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

all_matches_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_matches_button.click()

# select dropdown
dropdown = Select(driver.find_element(By.ID, "country"))
dropdown.select_by_visible_text("Spain")

time.sleep(5) # wait for page to load


date, home_team, score, away_team = [], [], [], []
matches = driver.find_elements(By.TAG_NAME, "tr")

for match in matches:

    # TAG_NAME
    date.append(match.find_elements(By.TAG_NAME, "td")[0].text) # == //tr/td[0]
    home_team.append(match.find_elements(By.TAG_NAME, "td")[1].text)
    score.append(match.find_elements(By.TAG_NAME, "td")[2].text)
    away_team.append(match.find_elements(By.TAG_NAME, "td")[3].text)

    ## XPATH
    # date.append(match.find_elements(By.XPATH, "./td[1]")[0].text) # == //tr/td[0]
    # home_team.append(match.find_elements(By.XPATH, "./td[2]")[0].text)
    # score.append(match.find_elements(By.XPATH, "./td[3]")[0].text)
    # away_team.append(match.find_elements(By.XPATH, "./td[4]")[0].text)

    print(date[-1], home_team[-1], score[-1], away_team[-1])


df = pd.DataFrame({"date": date, "home_team": home_team, "score": score, "away_team": away_team}) # create DataFrame
df.to_csv("Premier_league_matches.csv", index=False) # save to csv
print(df)