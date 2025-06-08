from pandas import DataFrame
from essentialkit import file_operations


def get_data(content):
    text = ""
    if content:
        print(content)
        for dictionary in content:
            # for key, value in dictionary.items():
            #     print(key, value)
            text += f"{dictionary['label']}\n{dictionary['value']}"
    return text


if __name__ == '__main__':

    info_raw = file_operations.read_json("../output/raw/data_12100_12200.json")

    data = {
        "ID": [],
        "Transliteración": [],
        "Fecha de Publicación": [],
        "Estado de Verificación": [],
        "Categoría Gramatical": [],
        "Ortografía Jeroglífica": [],
        "Traducción EN": [],
        "Traducción FR": [],
        "Cronología": [],
        "Comentario": [],
        "Diccionario": [],
        "Lexicons y Regular Indexes": [],
        "Further References": [],
        "Autor": []
    }

    for info in info_raw:
        data["ID"].append(info.get("id"))
        data["Transliteración"].append(info.get("transliteration"))
        data["Fecha de Publicación"].append(info.get("publication_date"))
        data["Estado de Verificación"].append(info.get("status"))
        data["Categoría Gramatical"].append(info.get("category"))
        data["Ortografía Jeroglífica"].append("\n".join(info.get("image")))
        data["Traducción EN"].append(info.get("EN"))
        data["Traducción FR"].append(info.get("FR"))
        data["Cronología"].append("\n".join(info.get("times")))
        data["Comentario"].append("\n".join(info.get("comment")))
        data["Diccionario"].append(get_data(info.get("DICTIONARIES")))
        data["Lexicons y Regular Indexes"].append(get_data(info.get("LEXICONS AND REGULAR INDEXES")))
        data["Further References"].append(get_data(info.get("FURTHER REFERENCES")))
        data["Autor"].append(info.get("author"))
    DataFrame(data).to_csv("../output/master/output_2025-06-08_.csv", index=False, sep=";")
