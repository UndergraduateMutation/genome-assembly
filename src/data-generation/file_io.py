def read_file_content(file_path: str) -> str:
    with open(file_path, "r", encoding= "ascii") as file:
        return file.read()

def write_to_file(file_path: str, content: str) -> None:
    with open(file_path, "w", encoding= "ascii") as file:
        file.write(content)
