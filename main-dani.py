import requests
from selenium.webdriver.common.by import By
from appvega import constants


def descargar_imagen(url, nombre_archivo):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza una excepción si hubo un error en la descarga

        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(respuesta.content)

        print(f"Imagen descargada y guardada como: {nombre_archivo}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")


if __name__ == "__main__":

    # url = "https://app.vega-lexique.fr/api/files/4c618868-80d7-4e84-9d95-065f2a4d55d7.svg"
    # descargar_imagen(url, "output/imagen_descargada.svg")

    div = driver.find_element(by=By.CLASS_NAME, value=constants.CLASS_OF_DATA)
    info = div.find_element(by=By.CLASS_NAME, value=constants.CLASS_OF_INFO).text
    stack = div.find_element(by=By.CLASS_NAME, value=constants.CLASS_OF_STACK).text
    entry = stack.find_elements(by=By.TAG_NAME, value="div") # deben obtenerse 5
    title = entry[0].find_element(by=By.CLASS_NAME, value="entry-transliteration").text
    style = entry[0].find_element(by=By.CLASS_NAME, value="graphy-image-bg").get_attribute("style")
    # Extrae la URL del estilo CSS
    inicio = style.find('url("') + 5
    fin = style.find('")')
    url = style[inicio:fin]
    translations = entry[1].find_elements(by=By.CLASS_NAME, value="entry-nuance") # debe haber 4

    data = {
        "title": title,
        "image": url, #Hieroglyphic spellings
        "DE": translations[0],
        "AR": translations[1],
        "EN": translations[2],
        "FR": translations[3],
    }
    
    
    
