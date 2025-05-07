BASE_PATH = 'input'

def read_lines_from_file(fileName):
  with open(f'{BASE_PATH}/{fileName}', 'r', encoding='utf-8') as file:
    return [line.strip() for line in file if line.strip()]
