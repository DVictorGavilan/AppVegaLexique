import requests


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

    url = "https://app.vega-lexique.fr/api/files/4c618868-80d7-4e84-9d95-065f2a4d55d7.svg"
    descargar_imagen(url, "output/imagen_descargada.svg")
