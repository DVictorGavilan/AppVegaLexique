import requests
from essentialkit import file_operations

def descargar_imagen(url, nombre_archivo):

    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza una excepción si hubo un error en la descarga

        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(respuesta.content)

        print(f"Imagen descargada y guardada como: {nombre_archivo}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")


if __name__ == '__main__':

    files_data =[]

    for file in file_operations.get_all_file_paths_in_directory("output"):
        if "json" in file:
            file_data = file_operations.read_json(file)
            files_data += file_data

    for f in file_data:

        descargar_imagen(f.get("image"), f"output/images/{f.get('id')}.svg")
