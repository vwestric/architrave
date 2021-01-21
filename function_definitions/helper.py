#Helper Functions
def load_csv(file_path, file_name, delimiter="|", encoding="utf-8"):
    import csv
    with open(file_path + file_name, "r", encoding=encoding) as file:
        reader = list(csv.reader(file, delimiter=delimiter))

    return reader


def load_json(file_path, file_name):
    import json
    with open(file_path + file_name, "r", encoding="utf-8", errors="ignore") as file:
        data = json.load(file)
    return data


def load_data(file_path, file_name, delimiter="|", encoding="utf-8"):
    if ".csv" in file_name:
        return load_csv(file_path, file_name, delimiter, encoding)
    elif ".json" in file_name:
        return load_json(file_path, file_name)


def write_csv(file_path, file_name, data, seperator="|"):
    if isinstance(data, dict):
        with open(file_path + file_name, "w", encoding="utf-8") as file:
            for key, value in data.items():
                file.write(key + seperator + str(value) + "\n")
    elif isinstance(data, list):
        with open(file_path + file_name, "w", encoding="utf-8") as file:
            for row in data:
                if isinstance(row, list):
                    file.write(seperator.join(row) + "\n")
                else:
                    file.write(row + "\n")


def write_json(file_path, file_name, data):
    import json
    with open(file_path + file_name, "w", encoding="utf-8", errors="ignore") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def crawler_xml(file_path):
    from bs4 import BeautifulSoup
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    doc = BeautifulSoup(content, "xml")
    return doc