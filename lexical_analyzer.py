from typing import Callable, List, Optional

from utils.file_helper import delete_if_exists, read_lines_from_file
from utils.token_match import TokenMatch
from utils.token_enum import TokenEnum

INPUT_FILE_NAME = 'input-2.por'

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
    match_token_keywords,
    match_token_atr,
    match_token_logoperators,
    match_token_mathoperators,
    match_token_parentheses,
    match_token_constnumbers,
    match_token_identifier,
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
        new_line = new_line[:match.start] + " " + match.replacement + " " + new_line[match.end:]
        i = match.start + len(match.replacement) + 2 # Count spaces separators
        match_found = True
        break # Exit after match

    if not match_found:
      # Commented until all token matchers are completed
      # current_char = new_line[i]
      # if not current_char.isspace():
      #   raise Exception(f"Unknown token '{current_char}' at line {lineNumber}:{i}")

      i += 1

  # Collapse multiple spaces into a single space and trim the line
  new_line = ' '.join(new_line.split())
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

def match_token_keywords(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  def is_valid_boundary(start: int, end: int) -> bool:
    prev_valid = start == 0 or not line[start - 1].isalnum()
    next_valid = end >= len(line) or not line[end].isalnum()
    return prev_valid and next_valid

  keywords = {
    "até": TokenEnum.ATE,
    "e": TokenEnum.E,
    "então": TokenEnum.ENTAO,
    "escreva": TokenEnum.ESCREVA,
    "fim_para": TokenEnum.FIMPARA,
    "fim_se": TokenEnum.FIMSE,
    "leia": TokenEnum.LEIA,
    "não": TokenEnum.NAO,
    "ou": TokenEnum.OU,
    "para": TokenEnum.PARA,
    "passo": TokenEnum.PASSO,
    "se": TokenEnum.SE,
    "senão": TokenEnum.SENAO,
    "inteiro": TokenEnum.TIPO,
  }

  for keyword, token in keywords.items():
    length = len(keyword)
    if line[startIndex:startIndex + length].lower() == keyword:
      if is_valid_boundary(startIndex, startIndex + length):
        return TokenMatch(start=startIndex, end=startIndex + length, replacement=token.name)
  
  return None  # Not a match

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

def match_token_mathoperators(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  char = line[startIndex]

  if char == '+':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.OPMAIS.name)
  if char == '-':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.OPMENOS.name)
  if char == '*':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.OPMULTI.name)
  if char == '/':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.OPDIVI.name)

  return None  # Not a match

def match_token_parentheses(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  char = line[startIndex]

  if char == '(':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.PARAB.name)
  if char == ')':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.PARFE.name)

  return None  # Not a match

def match_token_constnumbers(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  if not line[startIndex].isdigit():
    return None  # Not starting with a digit

  i = startIndex
  while i < len(line) and line[i].isdigit():
    i += 1

  # Check token boundaries
  prev_valid = startIndex == 0 or not line[startIndex - 1].isalnum()
  next_valid = i >= len(line) or not line[i].isalnum()

  if prev_valid and next_valid:
    return TokenMatch(start=startIndex, end=i, replacement=TokenEnum.NUMINT.name)

  return None  # Not a match

def match_token_identifier(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  char = line[startIndex]
  if not (char.isalpha() or char == '_'):
    return None  # Identifiers must start with a letter or underscore

  i = startIndex + 1
  while i < len(line) and (line[i].isalnum() or line[i] == '_'):
    i += 1

  prev_valid = startIndex == 0 or not line[startIndex - 1].isalnum()
  next_valid = i >= len(line) or not line[i].isalnum()
  if prev_valid and next_valid:
    return TokenMatch(start=startIndex, end=i, replacement=TokenEnum.ID.name)

  return None  # Not a valid standalone identifier

if __name__ == "__main__":
  main()