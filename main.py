import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

FORM = "https://docs.google.com/forms/d/e/1FAIpQLSfoikPIOuyU7L7IyWCBJDugk7Um4wXMMUgdtK97vWWizDekbw/viewform?usp=sf_link"
URL = ""
response = requests.get(URL)
sp = BeautifulSoup(response.content, "lxml")

# scrape for links of apartments
links_elements = sp.select(".StyledPropertyCardDataWrapper a")
links = [link["href"] for link in links_elements]

# scrape for prices
price_elements = sp.select(".PropertyCardWrapper span")
prices = [price.get_text().replace("/mo", "").split("+")[0] for price in price_elements if "$" in price.text]

# scrape for address
address_elements = sp.select(".StyledPropertyCardDataWrapper address")
all_address = [address.get_text().replace("|", " ").strip() for address in address_elements]

# Use Selenium to fill up form to create doc.
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)

for i in range(len(links)):
    driver.get(FORM)
    time.sleep(3)

    address_form = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                                 '1]/div/div[1]/input')
    price_form = driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                              '1]/div/div[1]/input')
    links_form = driver.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div["
                                              "1]/div/div[1]/input")
    button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address_form.send_keys(all_address[i])
    price_form.send_keys(prices[i])
    links_form.send_keys(links[i])
    button.click()

