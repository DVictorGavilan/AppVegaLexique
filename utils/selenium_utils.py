import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
