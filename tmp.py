import pandas
import pandas as pd
from essentialkit import file_operations


def lista_a_dataframe(lista):
    """
    Toma una lista y devuelve un DataFrame con dos columnas:
    - 'Impares': elementos en índices impares
    - 'Pares': elementos en índices pares

    Si las listas tienen diferente longitud, se rellena con None.
    """
    impares = [lista[i] for i in range(len(lista)) if i % 2 == 1]
    pares = [lista[i] for i in range(len(lista)) if i % 2 == 0]

    # Igualar longitudes rellenando con None
    max_len = max(len(impares), len(pares))
    impares += [None] * (max_len - len(impares))
    pares += [None] * (max_len - len(pares))

    df = pd.DataFrame({
        'Impares': impares,
        'Pares': pares
    })

    return df


import json


def lista_a_json(lista):
    """
    Toma una lista y devuelve un diccionario (json) donde:
    - claves: elementos en índices impares (1, 3, 5, ...)
    - valores: elementos en índices pares anteriores (0, 2, 4, ...)
    Si la lista tiene longitud impar, el último valor se descarta.
    """
    # Emparejamos elementos en índices pares con los impares siguientes
    diccionario = {str(lista[i + 1]): lista[i] for i in range(0, len(lista) - 1, 2)}

    return diccionario



def read_txt_file(file_path):
    """
    Reads the content of a .txt file and returns it as a string.

    Parameters:
        file_path (str): The path to the .txt file.

    Returns:
        str: Content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == '__main__':
    data = {}
    txt = read_txt_file("VegaLexique - Hoja 1.tsv")
    for i in txt:
        line = i.split("\t")

        data[line[0]] = line[1].replace("\n", "")

    # df = lista_a_dataframe(dictionaries)
    # data = lista_a_json(dictionaries)
    # df.to_csv("dictionary.csv", index=False, sep=";")
    file_operations.write_json(data=data, output_path="dictionary.json")
