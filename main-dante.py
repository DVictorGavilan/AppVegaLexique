import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from appvega.selenium_utils import start_browser, hover_element
from appvega import constants


TARGET_SVG = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]" # Nueva URL

def main(target_url):
    driver = start_browser()
    driver.get(target_url)
    time.sleep(2)

    try:
        svg_element = driver.find_element(By.XPATH, TARGET_SVG)
        actions = ActionChains(driver)
        actions.move_to_element(svg_element).perform()
        print("Hover sobre SVG realizado con éxito")
    except Exception as e:
        print(f"Error: {e}")

    try:
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
    style = entry[0].find_element(by=By.CLASS_NAME, value="graphy-image-bg").get_attribute("style")
    # Extrae la URL del estilo CSS
    inicio = style.find('url("') + 5
    fin = style.find('")')
    url = style[inicio:fin]
    translations = stack.find_elements(by=By.CLASS_NAME, value="entry-nuance")  # debe haber 4
    labels = stack.find_elements(by=By.CLASS_NAME, value="entry-dictionary-label")
    values = stack.find_elements(by=By.CLASS_NAME, value="entry-dictionary-value")
    dictionary = res = {label.text: value.text for label, value in zip(labels, values)}
    try:
        comment = stack.find_element(by=By.ID, value="comments").text
    except:
        comment = "........N/A"

    data = {
        "id": info.split(" | ")[-1],
        "title": title,
        "image": f"https://app.vega-lexique.fr/{url}",  #Hieroglyphic spellings
        "DE": translations[0].text,
        "AR": translations[1].text,
        "EN": translations[2].text,
        "FR": translations[3].text,
        "comment": comment[8:]
    }
    data.update(dictionary)
    return data

    time.sleep(2)


if __name__ == "__main__":
    vega_raw = []
    for i in range(2200, 2300):
        try:
            vega_raw.append(main(f"https://app.vega-lexique.fr/?entries=w{i}"))
            print(i)
        except:
            continue
    with open('output/raw/data_200_300.json', 'w', encoding="utf-8") as file:
        json.dump(vega_raw, file, ensure_ascii=False, indent=2)


