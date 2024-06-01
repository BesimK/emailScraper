import time
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.locators import Locators


def get_tools():

    options = Options()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")  # Set window size


    driver = webdriver.Chrome(options=options)
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.google.com/maps?hl=en')
    return driver, wait, action


def take_screenshot(driver, name):
    driver.save_screenshot(f"{name}.png")


def fill_the_list(driver, action):
    counter = 0
    pos = 3
    business_details = []
    while True:
        xpath = f"//div[1]/div[{pos}]/div[1]/a[1]"
        LIST_ELEMENT = (By.XPATH, xpath)
        if counter / 100 == 1:
            time.sleep(10)
            counter = 0
        try:
            element = driver.find_element(*LIST_ELEMENT)
            action.move_to_element(element).perform()
            time.sleep(1)
            action.click(element).perform()
            time.sleep(2)
            title = driver.find_element(By.XPATH, '//div[1]/div[1]/h1[1]').text
            print(title)
            counter += 1
            pos = pos + 2
            time.sleep(2)
            name = 1
            phone = 2
            website = 3
            address = 4
            business_details.append(
                {'Name': name, 'Phone Number': phone, 'Website Address': website, 'Address': address})

        except Exception:
            action.key_down(Keys.ARROW_DOWN).perform()
            time.sleep(1)
            action.release().perform()
            take_screenshot(driver, f"debug{counter}")
            break

    return business_details


def scrape_google_maps(neighborhood, business_type):
    driver, wait, action = get_tools()

    search_box = driver.find_element(*Locators.SEARCH_BOX)
    search_box.send_keys(neighborhood + Keys.RETURN)
    driver.implicitly_wait(10)

    wait.until(EC.element_to_be_clickable(Locators.NEAR_BUTTON)).click()

    search_box = driver.find_element(*Locators.SEARCH_BOX)
    search_box.send_keys(business_type + Keys.RETURN)

    time.sleep(5)
    business_details = fill_the_list(driver, action)
    print(business_details)
    driver.quit()


scrape_google_maps("Biga", "Diş Hekimi")
