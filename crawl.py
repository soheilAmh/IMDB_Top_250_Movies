from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

browser = webdriver.Firefox()
browser.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')

movies = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.with-margin a')))
movie_urls = [m.get_attribute('href') for m in movies]
movie_urls = list(dict.fromkeys(movie_urls))

while(len(movie_urls) != 250):
    movies = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.with-margin a')))
    movie_urls = [m.get_attribute('href') for m in movies]
    movie_urls = list(dict.fromkeys(movie_urls))

print(f"Found {len(movie_urls)} movie links")

all_data = []
i = 1
for url in movie_urls:
    browser.get(url)
    time.sleep(1)

    Title = WebDriverWait(browser, 5).until(
    EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "hero__primary-text")]'))).text

    Year = WebDriverWait(browser, 5).until(
    EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "rdat")]'))).text
    
    try:
        Parental_guide = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH,'//a[contains(@href, "parentalguide") and contains(@href, "certificates")]'))).text
    except:
        Parental_guide = "N/A"

    try :
        Runtime = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH,'//li[@role="presentation" and contains(text(), "m") or contains(text(), "h")]'))).text
    except:
        Runtime = -1

    Genres = WebDriverWait(browser, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@class, "ipc-chip--on-baseAlt")]')))
    Genre_list = [g.text for g in Genres]

    try:
        Directors = WebDriverWait(browser, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[@data-testid="title-pc-principal-credit"][.//span[text()="Directors"] or .//span[text()="Director"]]//a')))
        Director_list = [d.text for d in Directors if d.text.strip()]
    except:
        Director_list = "N/A"

    Writers = WebDriverWait(browser, 5).until(
    EC.presence_of_all_elements_located((By.XPATH, '//li[@data-testid="title-pc-principal-credit"][.//span[text()="Writers"] or .//span[text()="Writer"] or .//a[text()="Writer"] or .//a[text()="Writers"]]//a')))
    Writer_list = [w.text for w in Writers if w.text.strip()]
    if 'Writers' in Writer_list:
        Writer_list.remove('Writers')
    if 'Writer' in Writer_list:
        Writer_list.remove('Writer')

    try:
        Stars = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[@data-testid="title-pc-principal-credit"][.//a[text()="Stars"] or .//span[text()="Star"]]//div//a')))
        Star_list = [s.text for s in Stars if s.text.strip()]
    except:
        Star_list = "N/A"

    try:
        Gross_US_Canada = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-testid="title-boxoffice-grossdomestic"]//span[contains(@class,"ipc-metadata-list-item__list-content-item")]')))
        Gross_US_Canada_value = Gross_US_Canada.text.strip()
    except:
        Gross_US_Canada_value = "N/A"

    x = url.find('/tt')
    movie_data = {
        'Title': Title,
        'Year': Year,
        'ParentalGuide': Parental_guide,
        'Runtime': Runtime,
        'Genres': Genre_list,
        'Directors': Director_list,
        'Writers': Writer_list,
        'Stars': Star_list,
        'GrossUSCanada': Gross_US_Canada_value,
        'MovieID': url[x+3:x+10]
    }

    all_data.append(movie_data)

    print(f"Scraped: movie {i} Done")
    i += 1

df = pd.DataFrame(all_data)

df.to_excel('imdb_top250.xlsx', index=False)