import time
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.locators import Locators
from utils.email_crawler import EmailCrawler


def get_tools():
    options = Options()
    options.add_argument("--headless")  # Headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  # Set window size

    driver = webdriver.Chrome(options=options)
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 30)
    driver.get('https://www.google.com/maps?hl=en')
    return driver, wait, action


def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    time.sleep(1)  # Give time for the page to scroll and element to become visible


def fill_the_list(driver, action, wait):
    counter = 0
    pos = 3
    business_details = []
    while True:
        xpath = f"//div[1]/div[{pos}]/div[1]/a[1]"
        LIST_ELEMENT = (By.XPATH, xpath)
        if counter != 0 and counter % 120 == 0:
            return business_details
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
                if website != "N/A" and not website.__contains__("instagram"):
                    crawler = EmailCrawler("http://" + website)
                    dum = crawler.get_emails()
                    if dum.length != 0:
                        email = dum

            except:
                pass

            business_details.append(
                {'Name': name, 'Phone Number': phone, 'Website Address': website, 'Address': address,
                 'Email': email})
        except:
            break

    for biz in business_details:
        print(biz)

    return business_details


def scrape_google_maps(neighborhood, business_type):
    driver, wait, action = get_tools()

    search_box = wait.until(EC.presence_of_element_located(Locators.SEARCH_BOX))
    search_box.send_keys(neighborhood + Keys.RETURN)
    wait.until(EC.element_to_be_clickable(Locators.NEAR_BUTTON)).click()

    search_box = wait.until(EC.presence_of_element_located(Locators.SEARCH_BOX))
    search_box.send_keys(business_type + Keys.RETURN)

    time.sleep(5)
    business_details = fill_the_list(driver, action, wait)
    driver.quit()

    return business_details
