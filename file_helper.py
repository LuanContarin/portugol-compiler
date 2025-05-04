def read_lines_from_file(filename):
  with open(filename, 'r', encoding='utf-8') as file:
    return [line.strip() for line in file if line.strip()]
