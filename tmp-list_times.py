from essentialkit import file_operations


if __name__ == '__main__':

    data = file_operations.read_json("output/raw/data_title_200_300.json")
    for value in data:
        id_ = value["id"]
        for time in value["times"]:
            print(id_, time, f"{id_}{time}", sep=",")
