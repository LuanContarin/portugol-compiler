import json
import os
from typing import Callable, List, Optional

from utils.file_helper import read_lines_from_file
from utils.token_match import TokenMatch
from utils.token_enum import TokenEnum

OUTPUT_PATH_BASE = 'output/lexic_analyzer'

class LexicalError(Exception):
  pass

def compile(fileName: str) -> List[str]:
  print('(Lexer started)')

  os.makedirs(OUTPUT_PATH_BASE, exist_ok=True)
  lines = read_lines_from_file(fileName)

  lexeme_pairs = []

  tokens_file_name = f'{fileName}_lexic-replaced.tem'
  with open(f'{OUTPUT_PATH_BASE}/{tokens_file_name}', 'w', encoding='utf-8') as tokens_file:
    # Scan and write each line
    for i, line in enumerate(lines):
      print(f'Scanning line [{i+1}]...\t{line.strip()}')
      (new_line, token_lexem) = scan_line(line, i+1)
      tokens_file.write(new_line + '\n')
      lexeme_pairs.extend(token_lexem)

  pairs_file_name = f'{fileName}_lexic-lexems.tem'
  with open(f'{OUTPUT_PATH_BASE}/{pairs_file_name}', 'w', encoding='utf-8') as lexeme_file:
    json.dump(lexeme_pairs, lexeme_file, ensure_ascii=False, indent=2)
    
  print(f'Output written to {OUTPUT_PATH_BASE}')
  print('(Lexer ended)')
  return lexeme_pairs

def scan_line(line: str, lineNumber: int) -> tuple[str, List[str]]:
  token_matchers: List[Callable[[str, int], Optional[TokenMatch]]] = [
    match_token_string,
    match_token_keywords,
    match_token_atr,
    match_token_logoperators,
    match_token_mathoperators,
    match_token_parentheses,
    match_token_constnumbers,
    match_token_separators,
    match_token_identifier,
    # ...
  ]

  i = 0
  new_line_parts = []
  token_lexem = []

  while i < len(line):
    # Skip spaces
    if line[i].isspace():
      new_line_parts.append(' ')
      i += 1
      continue

    match_found = False
    
    # Run all token matchers
    for matcher in token_matchers:
      match = matcher(line, i, lineNumber)
      if match:
        # Line replacement
        new_line_parts.append(f' {match.replacement} ')

        # Token-lexeme
        lexeme = line[match.start:match.end]
        token_lexem.append({
          "token": match.replacement,
          "lexeme": lexeme,
          "code_index": f'{lineNumber}:{match.start + 1}'
        })

        i = match.end
        match_found = True
        break # Exit after match

    if not match_found:
      # Unknown char
      raise LexicalError(f'Unknown char "{line[i]}" at line {lineNumber}:{i+1}')

  # Collapse multiple spaces into single space and trim the line
  new_line = ' '.join(''.join(new_line_parts).split())
  return (new_line, token_lexem)

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
    raise LexicalError(f'Unterminated string starting at line {lineNumber}:{startIndex}')

  end_index = i + 1
  return TokenMatch(start=startIndex, end=end_index, replacement=TokenEnum.STRING.name)

def match_token_keywords(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  def is_valid_boundary(start: int, end: int) -> bool:
    prev_valid = start == 0 or not line[start - 1].isalnum()
    next_valid = end >= len(line) or not line[end].isalnum()
    return prev_valid and next_valid

  keywords = {
    'até': TokenEnum.ATE,
    'e': TokenEnum.E,
    'então': TokenEnum.ENTAO,
    'escreva': TokenEnum.ESCREVA,
    'fim_para': TokenEnum.FIMPARA,
    'fim_se': TokenEnum.FIMSE,
    'leia': TokenEnum.LEIA,
    'não': TokenEnum.NAO,
    'ou': TokenEnum.OU,
    'para': TokenEnum.PARA,
    'passo': TokenEnum.PASSO,
    'se': TokenEnum.SE,
    'senão': TokenEnum.SENAO,
    'inteiro': TokenEnum.TIPO,
    # Additional Tokens (not in documentation)
    'algoritmo': TokenEnum.ALGORITMO,
    'var': TokenEnum.VAR,
    'inicio': TokenEnum.INICIO,
    'fimalgoritmo': TokenEnum.FIMALGORITMO,
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

def match_token_separators(line: str, startIndex: int, lineNumber: int) -> Optional[TokenMatch]:
  char = line[startIndex]

  if char == ':':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.COLON.name)
  if char == ',':
    return TokenMatch(start=startIndex, end=startIndex + 1, replacement=TokenEnum.COMMA.name)

  return None  # Not a valid standalone identifier

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
