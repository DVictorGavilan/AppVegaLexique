import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from appvega.selenium_utils import start_browser, hover_element



TARGET_URL = "https://app.vega-lexique.fr/?entries=w1144"
TARGET_SVG = "/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[1]" # Nueva URL

def main():
    driver = start_browser()
    driver.get(TARGET_URL)
    time.sleep(10)

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

    time.sleep(10)

if __name__ == "__main__":
    main()
