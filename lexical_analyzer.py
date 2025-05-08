from typing import Callable, List, Optional

from utils.file_helper import delete_if_exists, read_lines_from_file
from utils.token_match import TokenMatch
from utils.token_enum import TokenEnum

INPUT_FILE_NAME = 'input.por'

def main():
  lines = read_lines_from_file(INPUT_FILE_NAME)

  file_name = f'{INPUT_FILE_NAME}_lexic-output.txt'
  file_path = f'output/{file_name}'

  try:
    with open(file_path, 'w') as output_file:
      # Scan and write each line
      for i, line in enumerate(lines):
        print(f'Scanning line [{i+1}]...\t{line}')
        new_line = scan_line(line, i+1)
        output_file.write(new_line + '\n')
    
    print(f'Output written to {file_path}')
  except Exception as e:
    print(f'[COMPILATION ERROR] Lexical analysis failed:\n\t{e}')
    delete_if_exists(file_path)
  

def scan_line(line: str, lineNumber: int) -> str:
  token_matchers: List[Callable[[str, int], Optional[TokenMatch]]] = [
    match_token_string,
    match_token_atr,
    match_token_logoperators,
    # ...
  ]

  i = 0
  new_line = line

  while i < len(new_line):
    match_found = False
    
    # Run all token matchers
    for matcher in token_matchers:
      match = matcher(new_line, i, lineNumber)
      if match:
        new_line = new_line[:match.start] + match.replacement + new_line[match.end:]
        i = match.start + len(match.replacement)
        match_found = True
        break # Exit after match

    if not match_found:
      # Commented until all token matchers are completed
      # current_char = new_line[i]
      # if not current_char.isspace():
      #   raise Exception(f"Unknown token '{current_char}' at line {lineNumber}:{i}")

      i += 1

  return new_line

# ------------------------
# Token Matchers
# ------------------------
def match_token_string(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  if line[startIndex] != '"':
    return None  # Not a match

  i = startIndex + 1
  while i < len(line):
    if line[i] == '"' and line[i - 1] != '\\':
      break
    i += 1

  # Couldnt find string end
  if i >= len(line):
    raise Exception(f"Unterminated string starting at line {lineNumber}:{startIndex}")

  end_index = i + 1
  return TokenMatch(start=startIndex, end=end_index, replacement=TokenEnum.STRING.name)

def match_token_atr(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  if line[startIndex] != '<':
    return None  # Not a match
  
  next_char = line[startIndex + 1] if startIndex + 1 < len(line) else None
  if (next_char != '-'):
    return None  # Not a match
  
  return TokenMatch(start=startIndex, end=startIndex + 2, replacement=TokenEnum.ATR.name)

def match_token_logoperators(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  char = line[startIndex]
  next_char = line[startIndex + 1] if startIndex + 1 < len(line) else None
  
  # Multi-character logical operators
  if char == '<' and next_char == '>':
    return TokenMatch(start=startIndex, end=startIndex + 2, replacement=TokenEnum.LOGDIFF.name)
  if char == '<' and next_char == '=':
    return TokenMatch(start=startIndex, end=startIndex + 2, replacement=TokenEnum.LOGMENORIGUAL.name)
  if char == '>' and next_char == '=':
    return TokenMatch(start=startIndex, end=startIndex + 2, replacement=TokenEnum.LOGMAIORIGUAL.name)
  
  # Single-character logical operators
  if char == '=':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.LOGIGUAL.name)
  if char == '<':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.LOGMENOR.name)
  if char == '>':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.LOGMAIOR.name)
  
  return None  # Not a match

if __name__ == "__main__":
  main()