import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from appvega.selenium_utils import start_browser, hover_element
from appvega import constants
from pandas import DataFrame
from essentialkit import file_operations


def main(id_, target_url):
    driver = start_browser()
    driver.get(target_url)
    time.sleep(2)
    driver.find_element(by=By.CLASS_NAME, value="periods-overview").click()
    values = driver.find_elements(by=By.CLASS_NAME, value="periods-overview-sub-item")
    times = [value.text for value in values if value.get_attribute("data-selected") == "true" and value.text != '']
    return {
        "id": id_,
        "times": times
    }


if __name__ == '__main__':
    # data = []
    # inicial = 200
    # final = 300
    # for code in range(inicial, final):
    #     url = f"https://app.vega-lexique.fr/?entries=t{code}"
    #     try:
    #         data.append(main(id_=code, target_url=url))
    #     except:
    #         continue
    # with open(f'output/raw/data_title_{inicial}_{final}.json', 'w', encoding="utf-8") as file:
    #     json.dump(data, file, ensure_ascii=False, indent=2)
    data = file_operations.read_json("output/raw/data_title_200_300.json")
    DataFrame(data).to_csv(f"output/master/data_title_{200}_{300}.csv", index=False)