from file_helper import read_lines_from_file

# Table of tokens
# Token - Pattern (regex)
TOKEN_PATTERNS = [
  ('ATE', 'TODO'),
  ('ATR', 'TODO'),
]

INPUT_FILE_NAME = 'input.por'

def main():
  lines = read_lines_from_file(INPUT_FILE_NAME)
  for line_number, line in enumerate(lines, start=1):
    print(f"Line {line_number}: {line}")

if __name__ == "__main__":
  main()