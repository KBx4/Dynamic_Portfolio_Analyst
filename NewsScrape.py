from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import re


main_url = 'https://www.tickertape.in/stocks/'
tickers = ['icici-bank-ICBK']
headlines = []
all_urls = {}
stock = []
news_tables = []
for ticker in tickers:
    temp = []
    url = main_url + ticker
    driver = webdriver.Chrome()
    driver.get(url)
    def click_load_more():
        try:
            load_more_button = driver.find_element('xpath','//*[@id="load-more" and not(@disabled)]/button')
            load_more_button.click()
            time.sleep(1)  # Wait for content to load
            return True
        except:
            return False

    for i in range(60):
        click_load_more()
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    all_new_news = soup.find_all("a", class_="jsx-3440134818 news-card d-flex-col mb32")
    new_news_links = soup.find("div", class_="jsx-3440134818")
    new_links = new_news_links.find_all("a", href=True)
    for link in new_links:
        temp.append(link['href'])
    for news in all_new_news:
        headline = news.find('p', class_="shave-root").text
        news_tables.append(headline)
        stock.append(ticker)
    all_news = soup.find_all("a", class_="jsx-3953764037 news-card d-flex-row")
    all_links = soup.find("div", class_="jsx-3953764037")
    links = all_links.find_all('a', href=True)
    for link in links:
        temp.append(link['href'])
        #html_text = requests.get(link['href'])
        #print(html_text)
    for news in all_news:
        headline = news.find('p', class_="shave-root").text
        news_tables.append(headline)
        stock.append(ticker)
    all_urls[ticker] = temp
#print(news_tables)
#print(all_urls)
news_description = []
Date_time = []
for ticker in tickers:
    for link in all_urls[ticker]:
        if link != '#overlay-video':
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            desc = soup.find('meta', attrs={'name': 'description'})
            date = soup.find('meta', attrs={'property':'article:modified_time'})
            if date:
                time = date['content']
                time = time.replace('T',' ')
                if 'Z' in time:
                    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(?:\.\d+)?Z'
                    time = re.sub(pattern, r'\1', time)
                if '+05:30' in time:
                    pattern = r"\+\d{2}:\d{2}$"
                    time = re.sub(pattern, "", time)

                Date_time.append(time)
            else:
                Date_time.append('not available')

            if desc:
                description = desc['content']
                news_description.append(description)
            else:
                news_description.append('not available')

        else:
            news_description.append('not available')
            Date_time.append('not available')

dict = {'Date':Date_time, 'Stocks':stock, 'Headlines':news_tables, 'Description':news_description}
df = pd.DataFrame(dict)
df = df[(df['Date'] != 'not available')]
print(df)
df.to_csv('icici.csv')
