from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
# from dotenv import load_dotenv
# import os
# load_dotenv()
from bs4 import BeautifulSoup
import re
import requests

GOOGLE_SHEET = 'INSERT DOCS LINK'
HEMNET = 'https://www.zillow.com/wenatchee-wa/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A47.5150650462814%2C%22east%22%3A-119.87778908831359%2C%22south%22%3A47.28523555465401%2C%22west%22%3A-120.43191201311828%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A27836%2C%22regionType%22%3A6%7D%5D%2C%22mapZoom%22%3A12%7D'
LINK = 'https://www.zillow.com/'
headers = {
    'Accept-Language':'en-US,en;q=0.5',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'

}

class Crawler:
    def __init__(self) -> None:
        self.response = requests.get(HEMNET,headers=headers)
        self.zillow_page = self.response.text
        self.soup = BeautifulSoup(self.zillow_page, "html.parser")

    

    def beautiful(self):
        articles = self.soup.find_all(name="a", class_="property-card-link")
        self.articles_address = [item.get_text().replace(',', '') for item in articles if item.get_text().strip()]
        self.link = [item.get('href').replace(',', '') for item in articles if item.get_text().strip()]
        #Find Price
        price = self.soup.find_all('span', {'data-test': 'property-card-price'})
        self.article_price = [re.search(r"\$\d+", item.get_text().replace(',', '')).group() for item in price if item.get_text().strip()]

    
    def selenium_part(self):
        self.browser = webdriver.Firefox()
        self.browser.get(GOOGLE_SHEET)
        time.sleep(4)

    def fill_form(self):
        for i in range(len(self.link)):
            self.address_field = self.browser.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            self.address_field.send_keys(self.articles_address[i])
            self.price_field = self.browser.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            self.price_field.send_keys(self.article_price[i])
            if self.link[i][:2] == "/b":
                self.link_field = self.browser.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
                self.link_field.send_keys(f'{LINK}{self.link[i]}')
            else:
                self.link_field = self.browser.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
                self.link_field.send_keys(self.link[i])                
            self.click_skicka = self.browser.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
            self.click_skicka.click()
            time.sleep(2)
            more_answers = self.browser.find_element(By.LINK_TEXT,'Skicka ett annat svar')
            more_answers.click()
            time.sleep(4)


crawl_bot = Crawler()
crawl_bot.beautiful()
crawl_bot.selenium_part()
crawl_bot.fill_form()