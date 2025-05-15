from typing import Dict, List

from utils.token_enum import TokenEnum

END_OF_FILE = 'EOF'

def compile(lexemePairs: List[Dict[str, str]]):
  print('(Parser started)')

  print(lexemePairs)
  parser = Parser(lexemePairs)
  parser.parse()
  print('✅ Syntax is valid.')

  print('(Parser ended)')

class Parser:
  def __init__(self, tokens: List[Dict[str, str]]):
    self.tokens = tokens
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['token']
    
    return END_OF_FILE

  def match(self, expected: str):
    if self.current_token() == expected:
      self.pos += 1
      return
    
    actual = self.current_token()
    raise SyntaxError(f"Expected {expected}, got {actual} at position {self.pos}")

  def parse(self):
    self.match("ALGORITMO")
    self.match("STRING")

    if self.current_token() == "VAR":
      self.grammar_variable_block()

    self.match("INICIO")

    while self.current_token() not in ("FIMALGORITMO", "EOF"):
      self.statement()

    self.match("FIMALGORITMO")
    
  def statement(self):
    #   raise SyntaxError(f'Unexpected start of statement: {token}')
    return

  # ----------------
  # Grammars
  # ----------------
  def grammar_variable_block(self):
    self.match("VAR")

    while self.current_token() == "ID":
      self.match("ID")

      # Optional IDs separated by commas
      while self.current_token() == "COMMA":
        self.match("COMMA")
        self.match("ID")

      self.match("COLON")
      self.match("TIPO")

  # def grammar_assignment(self):
  #   self.match(TokenEnum.ID.name)
  #   self.match(TokenEnum.ATR.name)
  #   self.parse_expression()

