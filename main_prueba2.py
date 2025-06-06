import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appvega.selenium_utils import start_browser, click_element

def main_downloads_titles(target_url):
    print("Iniciando navegador...")
    driver = start_browser()
    wait = WebDriverWait(driver, 10)
    print("Navegador iniciado.")

    print(f"Cargando URL: {target_url}")
    driver.get(target_url)
    time.sleep(5)

    print("Buscando el título...")
    title_element = driver.find_element(By.XPATH,
                                        "/html/body/div[1]/div[2]/div/div[1]/div[2]/h2/span")
    title = title_element.text
    print(f"Título encontrado: {title}")

    print("Extrayendo imagen...")
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

    xpath_text_default = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[1]"
    xpath_selector_idiomas = '//div[@data-testid="entry-nuance-lang-menu"]//button[@data-testid="nuance-lang-selector"]'

    print("Extrayendo idioma por defecto...")
    idioma_default = None
    translation_default = None
    try:
        flag_selector = driver.find_element(By.CLASS_NAME, "nuance-flag-selector")
        flag_icon_span = flag_selector.find_element(By.XPATH, ".//span[contains(@class, 'flag-icon--')]")
        class_list = flag_icon_span.get_attribute("class").split()
        idioma_clase = [cls for cls in class_list if cls.startswith("flag-icon--") and cls != "flag-icon--medium"][0]
        idioma_default = idioma_clase.replace("flag-icon--", "").upper()
        translation_default = driver.find_element(By.XPATH, xpath_text_default).text
        print(f"Idioma por defecto detectado: {idioma_default}")
    except Exception as e:
        print(f"No se pudo detectar el idioma por defecto con selector, fallback texto: {e}")
        translation_default = driver.find_element(By.XPATH, xpath_text_default).text
        idioma_default = "DEFAULT"
        print(f"Idioma por defecto fallback: {translation_default}")

    data = {
        "url": target_url,
        "title": title,
        "image": images,
        idioma_default: translation_default,
        "DE": None,
        "FR": None,
        "EN": None
    }

    # Solo si existe selector de idioma intentamos cambiar idioma
    if idioma_default != "DEFAULT":
        try:
            print("Intentando cambiar a idioma Alemán...")
            idiom_selector = driver.find_element(By.XPATH, xpath_selector_idiomas)
            idiom_selector.click()
            time.sleep(1)

            flag_de = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flag-icon--de"))
            )
            driver.execute_script("arguments[0].click();", flag_de)
            time.sleep(2)

            translation_de = driver.find_element(By.XPATH, xpath_text_default).text
            print(f"Idioma Alemán: {translation_de}")
            data["DE"] = translation_de
        except Exception as e:
            print(f"No se pudo clickear en idioma Alemán: {e}")

        try:
            print("Intentando cambiar a idioma Francés...")
            idiom_selector = driver.find_element(By.XPATH, xpath_selector_idiomas)
            idiom_selector.click()
            time.sleep(1)

            flag_fr = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flag-icon--fr"))
            )
            driver.execute_script("arguments[0].click();", flag_fr)
            time.sleep(2)

            translation_fr = driver.find_element(By.XPATH, xpath_text_default).text
            print(f"Idioma Francés: {translation_fr}")
            data["FR"] = translation_fr
        except Exception as e:
            print(f"No se pudo clickear en idioma Francés: {e}")

            # Cambio a Inglés (UK)
        try:
            print("Intentando cambiar a idioma Inglés (UK)...")
            idiom_selector = driver.find_element(By.XPATH, xpath_selector_idiomas)
            idiom_selector.click()
            time.sleep(1)

            flag_en = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "flag-icon--en"))
            )
            driver.execute_script("arguments[0].click();", flag_en)
            time.sleep(2)

            translation_en = driver.find_element(By.XPATH, xpath_text_default).text
            print(f"Idioma Inglés (UK): {translation_en}")
            data["EN"] = translation_en
        except Exception as e:
            print(f"No se pudo clickear en idioma Inglés (UK): {e}")

    driver.quit()
    print("Navegador cerrado.")
    return data


if __name__ == "__main__":
    url = "https://app.vega-lexique.fr/?entries=t233"
    resultado = main_downloads_titles(url)
    print("Resultado final:", resultado)