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
    time.sleep(5)  # más tiempo para carga

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

    # Obtener idioma por defecto
    print("Extrayendo idioma por defecto...")
    default_element = driver.find_element(By.XPATH, xpath_text_default)
    translation_default = default_element.text
    print(f"Idioma Default: {translation_default}")

    translation_de, translation_fr = None, None

    # --- Cambiar a Alemán ---
    print("Intentando cambiar a idioma Alemán...")
    try:
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
    except Exception as e:
        print(f"No se pudo clickear en idioma Alemán: {e}")

    # --- Cambiar a Francés ---
    print("Intentando cambiar a idioma Francés...")
    try:
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
    except Exception as e:
        print(f"No se pudo clickear en idioma Francés: {e}")

    data = {
        "url": target_url,
        "title": title,
        "image": images,
        "Default": translation_default,
        "DE": translation_de,
        "FR": translation_fr
    }

    driver.quit()
    print("Navegador cerrado.")
    return data


if __name__ == "__main__":
    url = "https://app.vega-lexique.fr/?entries=t467"
    resultado = main_downloads_titles(url)
    print("Resultado final:", resultado)
