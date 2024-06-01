import random
import time
import re
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.locators import Locators


def ddg_search(website):
    options = Options()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  # Set window size

    driver = webdriver.Chrome(options=options)
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    driver.get("https://www.duckduckgo.com/")
    email = []
    priv_dom = format_url(website)
    domains = ["@gmail.com", "@hotmail.com", "@yahoo.com", priv_dom]
    search_parameter = f'iletişim site:{website}'
    driver.find_element(*Locators.DDG_INPUT).send_keys(search_parameter + Keys.RETURN)
    text = driver.page_source
    email.append(find_address(text))

    for domain in domains:
        search_parameter = f'{domain} site:{website}'
        driver.find_element(*Locators.DDG_SEARCH_BOX).clear()
        driver.find_element(*Locators.DDG_SEARCH_BOX).send_keys(search_parameter + Keys.RETURN)
        text = driver.page_source
        email.append(find_address(text))

    driver.close()
    return email


def format_url(url):
    if "://" in url:
        domain = url.split("://")[1]
    else:
        domain = url
    if domain.startswith("www."):
        domain = domain[4:]
    return f"@{domain}"


def find_address(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)


def take_screenshot(driver, name):
    driver.save_screenshot(f"{name}.png")


a = ddg_search("tolgaersoy.av.tr")
print(a)
