from utils.file_helper import read_lines_from_file
from utils.token_table import TokenTable
import re

INPUT_FILE_NAME = 'input.por'
TOKEN_PATTERN = {
  TokenTable.STRING: r'"[^"\n]*"'
}

def main():
  lines = read_lines_from_file(INPUT_FILE_NAME)

  for line in enumerate(lines, start=1):
    temp_line = line
    temp_line = replace_token(line, TokenTable.STRING)
    print(temp_line)
    
def replace_token(line, token: TokenTable):
  if not isinstance(token, TokenTable):
    raise TypeError('token must be an instance of TokenTable Enum')
  
  new_line = re.sub(TOKEN_PATTERN[token], token.name, line)
  return new_line

if __name__ == "__main__":
  main()