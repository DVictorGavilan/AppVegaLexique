from pandas import DataFrame
from essentialkit import file_operations


if __name__ == '__main__':

    files_data = []
    for file in file_operations.get_all_file_paths_in_directory("output/raw"):
        if "json" in file:
            file_data = file_operations.read_json(file)
            files_data += file_data

    data = {
        "id": [],
        "title": [],
        "publication_date": [],
        "status": [],
        "image": [],
        "DE": [],
        "AR": [],
        "EN": [],
        "FR": [],
        "comment": [],
        "fuente de transliteración": []
    }

    for f in files_data:
        data["id"].append(f.get("id"))
        data["title"].append(f.get("title"))
        data["publication_date"].append(f.get("publication_date"))
        data["status"].append(f.get("status"))
        data["image"].append(f.get("image"))
        data["DE"].append(f.get("DE"))
        data["AR"].append(f.get("AR"))
        data["EN"].append(f.get("EN"))
        data["FR"].append(f.get("FR"))
        data["comment"].append(f.get("comment"))
        data["fuente de transliteración"].append(f.get("referencies"))
    DataFrame(data).to_csv("output/master/output_2025-06-03.csv", index=False)