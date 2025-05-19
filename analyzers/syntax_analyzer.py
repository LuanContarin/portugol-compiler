from typing import Dict, List

from utils.token_enum import TokenEnum

END_OF_FILE = '__EOF__'

class Parser:
  def __init__(self, tokens: List[Dict[str, str]]):
    self.tokens = tokens
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['token']
    
    return END_OF_FILE
  
  def current_lexeme(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['lexeme']
    
    raise SystemError('invalid call for lexeme')
  
  def current_code_index(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['code_index']
    
    raise SystemError('invalid call for code index')

  def match(self, expected: TokenEnum):
    if self.current_token() == expected.name:
      self.pos += 1
      return
    
    lexeme = self.current_lexeme()
    code_index = self.current_code_index()
    raise SyntaxError(f'Expected "{expected.value}", got "{lexeme}" at line {code_index}')
  
  def match_optional(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name
  
  def match_optional_any(self, expected: List[TokenEnum]) -> bool:
    return any(self.current_token() == t.name for t in expected)

  def parse(self):
    self.match(TokenEnum.ALGORITMO)
    self.match(TokenEnum.STRING)

    if self.match_optional(TokenEnum.VAR):
      self.grammar_variable_block()

    self.match(TokenEnum.INICIO)

    while self.current_token() not in (TokenEnum.FIMALGORITMO.name, END_OF_FILE):
      self.statement()

    self.match(TokenEnum.FIMALGORITMO)

  def statement(self):
    if self.match_optional(TokenEnum.ID):
      self.grammar_var_attribution()
    elif self.match_optional(TokenEnum.ESCREVA):
      self.grammar_command_escreva()
    elif self.match_optional(TokenEnum.LEIA):
      self.grammar_command_leia()
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Unexpected "{lexeme}" at line {code_index}')

  # ----------------
  # Grammars
  # ----------------
  def grammar_variable_block(self):
    self.match(TokenEnum.VAR)

    # In case there are no variables
    while self.match_optional(TokenEnum.ID):
      self.match(TokenEnum.ID)

      # Optional IDs separated by commas
      while self.match_optional(TokenEnum.COMMA):
        self.match(TokenEnum.COMMA)
        self.match(TokenEnum.ID)

      self.match(TokenEnum.COLON)
      self.match(TokenEnum.TIPO)

  def grammar_var_attribution(self):
    self.match(TokenEnum.ID)
    self.match(TokenEnum.ATR)
    self.grammar_op_expression()

  def grammar_command_escreva(self):
    self.match(TokenEnum.ESCREVA)
    self.match(TokenEnum.PARAB)

    # Terms supported by escreva
    if self.match_optional(TokenEnum.ID):
      self.match(TokenEnum.ID)
    elif self.match_optional(TokenEnum.NUMINT):
      self.match(TokenEnum.NUMINT)
    elif self.match_optional(TokenEnum.STRING):
      self.match(TokenEnum.STRING)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Unexpected "{lexeme}" in escreva at line {code_index}')

    self.match(TokenEnum.PARFE)

  def grammar_command_leia(self):
    self.match(TokenEnum.LEIA)
    self.match(TokenEnum.PARAB)

    # Terms supported by leia
    if self.match_optional(TokenEnum.ID):
      self.match(TokenEnum.ID)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Unexpected "{lexeme}" in leia at line {code_index}')

    self.match(TokenEnum.PARFE)

  #
  # Fundamental
  #
  def grammar_op_expression(self):
    self.grammar_op_term()
    
    while self.match_optional_any([TokenEnum.OPMAIS, TokenEnum.OPMENOS, TokenEnum.OPMULTI, TokenEnum.OPDIVI]):
      self.pos += 1
      self.grammar_op_term()

  def grammar_op_term(self):
    if self.match_optional(TokenEnum.ID):
      self.match(TokenEnum.ID)
    elif self.match_optional(TokenEnum.NUMINT):
      self.match(TokenEnum.NUMINT)
    elif self.match_optional(TokenEnum.PARAB):
      self.match(TokenEnum.PARAB)
      self.grammar_op_expression()
      self.match(TokenEnum.PARFE)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Expected identifier or value in expression at line {code_index}')
