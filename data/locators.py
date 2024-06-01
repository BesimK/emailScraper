from selenium.webdriver.common.by import By


class Locators:
    # Google Maps Locators
    SEARCH_BOX = (By.NAME, 'q')
    NEAR_BUTTON = (By.XPATH, "//div[text()= 'Nearby']")
    SECTION_RESULT_TITLE = (By.XPATH, '//div[1]/div[1]/h1[1]')
    SECTION_RESULT_ADDRESS = (By.XPATH, '//div[1]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]'
                                        '/div[1]/div[1]/div[2]/div[7]/div[3]/button[1]/div[1]/div[2]/div[1]')
    SECTION_RESULT_WEBSITE = (By.XPATH, '//div[1]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]'
                                        '/div[1]/div[1]/div[2]/div[7]/div[5]/a[1]/div[1]/div[2]/div[1]')
    SECTION_RESULT_PHONE_NUMBER = (By.XPATH,
                                   '//div[1]/div[3]/div[8]/div[9]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]'
                                   '/div[1]/div[2]/div[7]/div[4]/button[1]/div[1]/div[2]/div[1]')
    DDG_INPUT = (By.CSS_SELECTOR, '#searchbox_input')
    DDG_SEARCH_BOX = (By.CSS_SELECTOR, '#search_form_input')
