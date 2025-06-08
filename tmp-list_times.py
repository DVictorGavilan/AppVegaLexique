import requests
from pandas import DataFrame
from essentialkit import file_operations

import cairosvg

def svg_to_png_transparent(input_svg_path, output_png_path):
    """
    Convert an SVG image to a PNG image with transparent background.

    Parameters:
    - input_svg_path: str, path to the .svg file
    - output_png_path: str, path where the .png will be saved
    """
    cairosvg.svg2png(url=input_svg_path, write_to=output_png_path)

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

    # data = file_operations.read_json("output/raw/data_title_ok_name_200_300.json")
    # for d in data:
    #     for i, image in enumerate(d["image"]):
    #         descargar_imagen(image, f"output/images/title_{d['url'][-3:]}/image_{i}.svg")

    for image_path in file_operations.get_all_file_paths_in_directory("output/images"):
        print(image_path)
        # svg_to_png_transparent(image_path, f"{image_path[:-4]}.png")
