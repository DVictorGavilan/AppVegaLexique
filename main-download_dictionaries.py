import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from appvega.utils import start_browser, hover_element
from appvega import constants


def main(target_url):
    driver = start_browser()
    driver.get(target_url)
    time.sleep(2)
    values = driver.find_elements(by=By.TAG_NAME, value="p")
    for value in values:
        print(value.text)


if __name__ == '__main__':

    url = "https://vega-vocabulaire-egyptien-ancien.fr/liste-des-abreviations-bibliographiques-utilisees-dans-le-vega/"
    main(target_url=url)