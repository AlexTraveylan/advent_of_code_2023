def read_input_file(file_path: str):
    with open(file_path, mode="r", encoding="utf-8") as input_file:
        return input_file.readlines()
