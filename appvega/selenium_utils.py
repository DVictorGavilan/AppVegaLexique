import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def click_element(driver, by_selector, locator, timeout=10):
    """
    Espera a que un elemento sea clickeable y luego lo hace clic.

    :param driver: Instancia del navegador Selenium.
    :param by_selector: Tipo de selector (e.g., By.XPATH, By.CLASS_NAME).
    :param locator: Valor del selector (string).
    :param timeout: Tiempo máximo de espera en segundos (por defecto 10s).
    """
    try:
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by_selector, locator)))
        elemento.click()
        logging.info(f"✅ Se hizo clic en el elemento: {by_selector} = {locator}")
    except Exception as e:
        logging.error(f"❌ Error al hacer clic en el elemento {by_selector} = {locator}: {type(e).__name__} - {e}")


def hover_element(driver: WebDriver, element: WebElement) -> None:
    """
    Realiza un hover (pasar el cursor) sobre el elemento dado.

    :param driver: Instancia del navegador Selenium.
    :param element: WebElement al que se le pasará el cursor.
    """
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        logging.info("✅ Hover realizado sobre el elemento.")
    except Exception as e:
        logging.error(f"❌ Error realizando hover: {e}")


# Configuración básica del logging para mostrar mensajes por consola
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def start_browser():
    """Starts and returns a Chrome instance with custom settings."""
    logging.info("Iniciando el navegador...")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    logging.info("Navegador iniciado correctamente.")
    return driver

def accept_cookies(driver: WebDriver, xpath: str, timeout: int = 10) -> None:
    """
    Acepta las cookies si el botón está presente en la página y espera a que desaparezca.

    :param driver: Instancia del navegador Selenium.
    :param xpath: Ruta del botón de cookies.
    :param timeout: Tiempo máximo de espera antes de continuar.
    """
    try:
        aceptar_cookies = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        aceptar_cookies.click()
        logging.info("✅ Se aceptaron las cookies.")

        # Esperar hasta que el botón desaparezca después de hacer clic
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        logging.info("✅ Botón de cookies desapareció, continuando con la ejecución.")
    except Exception:
        logging.warning("⚠️ No se encontró el botón de cookies o ya estaba aceptado.")
