import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from appvega.selenium_utils import start_browser, hover_element
from appvega import constants


def main(f, target_url):
    driver = start_browser()
    driver.get(target_url)
    time.sleep(2)
    driver.find_element(by=By.CLASS_NAME, value="periods-overview").click()
    values = driver.find_elements(by=By.CLASS_NAME, value="periods-overview-sub-item")
    for value in values:
        print(f, value.text, value.get_attribute("data-selected"))


if __name__ == '__main__':

    for i in range(200, 300):
        url = f"https://app.vega-lexique.fr/?entries=t{i}"
        main(f=i, target_url=url)
