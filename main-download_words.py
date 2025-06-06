import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from appvega.selenium_utils import start_browser, hover_element
from appvega import constants
from essentialkit import file_operations


TARGET_SVG = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]"

dictionary_translations = file_operations.read_json("dictionary.json")


def main(target_url):
    driver = start_browser()
    driver.get(target_url)
    time.sleep(2)
    status = driver.find_element(by=By.CLASS_NAME, value="public-status").get_attribute("data-status")

    try:
        svg_element = driver.find_element(By.XPATH, TARGET_SVG)
        actions = ActionChains(driver)
        actions.move_to_element(svg_element).perform()
        print("Hover sobre SVG realizado con éxito")
    except Exception as e:
        print(f"Error: {e}")

    try:
        publication_date = driver.find_element(by=By.CLASS_NAME, value="entry-save-message").text
        # XPath del botón Print dentro del menú que aparece tras el hover
        print_button_xpath = '//div[@class="menu"]//button[contains(.,"Print")]'
        
        # Esperar un poco para que el menú aparezca
        time.sleep(2)
        
        print_button = driver.find_element(By.XPATH, print_button_xpath)
        print_button.click()
        print("Clic en botón Print realizado con éxito")
    except Exception as e:
        print(f"Error al hacer clic en Print: {e}")

    time.sleep(2)
    div = driver.find_element(by=By.CLASS_NAME, value=constants.CLASS_OF_DATA)
    info = div.find_element(by=By.CLASS_NAME, value=constants.CLASS_OF_INFO).text
    stack = div.find_element(by=By.CLASS_NAME, value=constants.CLASS_OF_STACK)
    entry = stack.find_elements(by=By.TAG_NAME, value="div")  # deben obtenerse 5
    title = entry[0].find_element(by=By.CLASS_NAME, value="entry-transliteration").text
    images = []
    list_of_images_raw = driver.find_element(By.CLASS_NAME, value="entry-main-graphies")
    list_of_images = list_of_images_raw.find_elements(By.CLASS_NAME, "graphy-image-bg")
    for image in list_of_images:
        style_attr = image.get_attribute("style")
        inicio = style_attr.find('url("') + 5
        fin = style_attr.find('")')
        partial_url = style_attr[inicio:fin]
        full_image_url = f"https://app.vega-lexique.fr/{partial_url}"
        print(f"URL de imagen: {full_image_url}")
        images.append(full_image_url)
    # print(url)
    translations = stack.find_elements(by=By.CLASS_NAME, value="entry-nuance")  # debe haber 4

    extra_infos = stack.find_elements(by=By.CLASS_NAME, value="entry-dictionary-group")
    out_info = {}
    for extra_info in extra_infos:
        title_extra_info = extra_info.find_element(by=By.CLASS_NAME, value="entry-dictionary-group-title")
        labels = extra_info.find_elements(by=By.CLASS_NAME, value="entry-dictionary-label")
        values = extra_info.find_elements(by=By.CLASS_NAME, value="entry-dictionary-value")
        # print(labels)
        # dictionary = {label.text: value.text for label, value in zip(labels, values)}
        detail = []
        for label in labels:
            if label.text in dictionary_translations.keys():
                detail.append(dictionary_translations.get(label.text))
            else:
                detail.append(label.text)
        out_info[title_extra_info.text] = [detail]

    try:
        comment = stack.find_element(by=By.ID, value="comments").text
    except:
        comment = "........N/A"

    data = {
        "id": info.split(" | ")[-1],
        "title": title,
        "publication_date": publication_date,
        "status": status,
        "image": images,
        "DE": translations[0].text,
        "AR": translations[1].text,
        "EN": translations[2].text,
        "FR": translations[3].text,
        "comment": comment[8:].replace("\n", "")
        # "referencies": referencies
    }
    # print(data)
    data.update(out_info)
    return data

    time.sleep(2)


if __name__ == "__main__":
    vega_raw = []
    inicial = 5668
    final = 5672
    for i in range(inicial, final):
        try:
            _ = main(f"https://app.vega-lexique.fr/?entries=w{i}")
            vega_raw.append(_)
            print(_)
        except Exception as e:
            print(e)
            continue
    with open(f'output/raw/data_{inicial}_{final}.json', 'w', encoding="utf-8") as file:
        json.dump(vega_raw, file, ensure_ascii=False, indent=2)


