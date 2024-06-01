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


def get_tools():
    options = Options()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  # Set window size

    driver = webdriver.Chrome(options=options)
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.google.com/maps?hl=en')
    return driver, wait, action


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)  # Give time for the page to scroll and element to become visible


def find_address(text):
    return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)


def format_url(url):
    if "://" in url:
        domain = url.split("://")[1]
    else:
        domain = url
    if domain.startswith("www."):
        domain = domain[4:]
    return f"@{domain}"


def ddg_search(driver, action, website):
    a = random.randint(1, 1000000)
    take_screenshot(driver, f'ddg_{a}')
    action.send_keys(Keys.CONTROL + "t")
    driver.get("https://www.duckduckgo.com/")
    email = set()
    priv_dom = format_url(website)
    domains = ["@gmail.com", "@hotmail.com", "@yahoo.com", "iletişim", priv_dom]
    for domain in domains:
        search_parameter = f'{domain} site:{website}'
        driver.find_element(*Locators.DDG_INPUT).send_keys(search_parameter)
        text = driver.page_source
        email.add(find_address(text))

    driver.close()
    return email


def take_screenshot(driver, name):
    driver.save_screenshot(f"{name}.png")


def fill_the_list(driver, action, wait):
    counter = 0
    pos = 3
    business_details = []
    while True:
        xpath = f"//div[1]/div[{pos}]/div[1]/a[1]"
        LIST_ELEMENT = (By.XPATH, xpath)
        if counter != 0 and counter % 100 == 0:
            time.sleep(10)
        try:
            element = wait.until(EC.presence_of_element_located(LIST_ELEMENT))
            scroll_to_element(driver, element)
            action.move_to_element(element).perform()
            time.sleep(1)
            element.click()
            time.sleep(3)
            title = driver.find_element(*Locators.SECTION_RESULT_TITLE).text
            print(f"<----- {str(counter + 1)}. Element Located  ---------->")
            counter += 1
            pos += 2
            time.sleep(2)
            name = title
            email = []
            phone, website, address = "N/A", "N/A", "N/A"
            try:
                phone = driver.find_element(*Locators.SECTION_RESULT_PHONE_NUMBER).text
            except:
                pass
            try:
                website = driver.find_element(*Locators.SECTION_RESULT_WEBSITE).text
            except:
                pass
            try:
                address = driver.find_element(*Locators.SECTION_RESULT_ADDRESS).text
            except:
                pass
            try:
                if website != "N/A" and website.__contains__(".com"):
                    email = ddg_search(driver, action, website)
            except:
                pass

            print(email)
            business_details.append(
                {'Name': name, 'Phone Number': phone, 'Website Address': website, 'Address': address,
                 'Email': email})

        except Exception as e:
            take_screenshot(driver, 'exception')
            print(f"Error: {e}")
            break

    return business_details


def scrape_google_maps(neighborhood, business_type):
    driver, wait, action = get_tools()

    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located(Locators.SEARCH_BOX))
    search_box.send_keys(neighborhood + Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(Locators.NEAR_BUTTON)).click()

    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located(Locators.SEARCH_BOX))
    search_box.send_keys(business_type + Keys.RETURN)

    time.sleep(5)
    business_details = fill_the_list(driver, action, wait)
    print(business_details)

    driver.quit()


scrape_google_maps("İstanbul", "Avukat")
