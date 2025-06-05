import time
from selenium.webdriver.common.by import By
from appvega.selenium_utils import start_browser,click_element

def main_downloads_titles(target_url):
    print("Iniciando navegador...")
    driver = start_browser()
    print("Navegador iniciado.")
    
    print(f"Cargando URL: {target_url}")
    driver.get(target_url)
    time.sleep(5)  # más tiempo para carga
    
    print("Buscando el título...")
    title_element = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/h2/span")
    title = title_element.text
    print(f"Título encontrado: {title}")

    print("Extrayendo imagen...")
    style_element = driver.find_element(By.CLASS_NAME, "graphy-image-bg")
    style_attr = style_element.get_attribute("style")
    inicio = style_attr.find('url("') + 5
    fin = style_attr.find('")')
    partial_url = style_attr[inicio:fin]
    full_image_url = f"https://app.vega-lexique.fr/{partial_url}"
    print(f"URL de imagen: {full_image_url}")

    # XPaths comunes
    xpath_traduccion = "/html/body/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[1]"
    xpath_selector_idiomas = '//div[@data-testid="entry-nuance-lang-menu"]//button[@data-testid="nuance-lang-selector"]'
    xpath_bandera_alemana = '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div[1]/button'
    xpath_bandera_francesa = '/html/body/div[1]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div/div/div[2]/button'

    print("Extrayendo Idioma del Reino Unido (UK)...")
    uk_element = driver.find_element(By.XPATH, xpath_traduccion)
    translation_uk = uk_element.text
    print(f"Idioma UK: {translation_uk}")

    print("Cambiando a idioma Alemán...")
    click_element(driver, xpath_selector_idiomas)
    time.sleep(1)
    click_element(driver, xpath_bandera_alemana)
    time.sleep(2)
    translation_de = driver.find_element(By.XPATH, xpath_traduccion).text
    print(f"Idioma Alemán: {translation_de}")

    print("Cambiando a idioma Francés...")
    click_element(driver, xpath_selector_idiomas)
    time.sleep(1)
    click_element(driver, xpath_bandera_francesa)
    time.sleep(2)
    translation_fr = driver.find_element(By.XPATH, xpath_traduccion).text
    print(f"Idioma Francés: {translation_fr}")

    data = {
        "url": target_url,
        "title": title,
        "image": full_image_url,
        "UK": translation_uk,
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
