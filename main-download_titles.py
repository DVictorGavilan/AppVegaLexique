import time
from selenium.webdriver.common.by import By
from appvega.utils import start_browser, click_element


def main_downloads_titles(target_url):
    print("Iniciando navegador...")
    driver = start_browser()
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

    # XPaths comunes
    xpath_text_default = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[1]"
    xpath_selector_idiomas = '//div[@data-testid="entry-nuance-lang-menu"]//button[@data-testid="nuance-lang-selector"]'
    #xpath_bandera_alemana = '//span[contains(@class, "flag-icon--de")]'
    #xpath_bandera_francesa = '//span[contains(@class, "flag-icon--fr")]'
    #xpath_bandera_uk = '//span[contains(@class, "flag-icon--en")]'

    translation_uk, translation_de, translation_fr = None, None, None

    print("Extrayendo Idioma por defecto..")
    default_element = driver.find_element(By.XPATH, xpath_text_default)
    translation = default_element.text
    print(f"Idioma Default: {translation}")

    print("Cambiando a idioma Alemán...")
    idiom = driver.find_elements(By.XPATH, xpath_selector_idiomas)
    if idiom:
        #(idiom[0],By.XPATH,xpath_selector_idiomas)
        idiom[0].click()
    time.sleep(1)

    idiom_al = driver.find_elements(By.CLASS_NAME, "flag-icon--de")
    if idiom_al:

        #click_element(idiom_al[0],By.CLASS_NAME,"flag-icon--de")
        idiom_al[0].find_element(By.XPATH, "../..").click()
        time.sleep(2)
        translation_de = driver.find_element(By.XPATH, xpath_text_default).text
        print(f"Idioma Alemán: {translation_de}")

    print("Cambiando a idioma Francés...")
    idiom = driver.find_elements(By.XPATH, xpath_selector_idiomas)
    if idiom:
        #click_element(idiom[0],By.XPATH,xpath_selector_idiomas)
        idiom[0].click()
    time.sleep(1)
    idiom_fr = driver.find_elements(By.CLASS_NAME, "flag-icon--fr")
    if idiom_fr:
        #click_element(idiom_fr[0],By.CLASS_NAME,"flag-icon--fr")
        idiom_fr[0].find_element(By.XPATH, "../..").click()

        time.sleep(2)
        translation_fr = driver.find_element(By.XPATH, xpath_text_default).text
        print(f"Idioma Francés: {translation_fr}")

    data = {
        "url": target_url,
        "title": title,
        "image": images,
        "Default": translation,
        "EN": translation_uk,
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
