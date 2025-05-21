from typing import Dict, List

from utils.token_enum import TokenEnum

class SemanticError(Exception):
  pass

class SemanticAnalyzer:
  def __init__(self, lexemePairs: List[Dict[str, str]]):
    self.lexeme_pairs = lexemePairs
    self.declared_vars = []
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['token']
    
    return TokenEnum.END_OF_FILE.name
  
  def current_lexeme(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['lexeme']
    
    return ' '
  
  def current_code_index(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['code_index']
    
    return self.lexeme_pairs[-1].get('code_index', 'unknown')

  def advance(self):
    self.pos += 1

  def check_token(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name

  def validate(self):
    self.get_declared_variables()
    self.validate_variable_usage()

  # ----------------
  # Validations
  # ----------------
  def get_declared_variables(self):
    in_var_block = False

    while self.pos < len(self.lexeme_pairs):
      # Identify the start of the var block
      if self.check_token(TokenEnum.VAR):
        in_var_block = True
      elif self.check_token(TokenEnum.INICIO):
        break
      elif in_var_block and self.check_token(TokenEnum.ID):
        lexeme = self.current_lexeme()

        if self.is_variable_declared(lexeme):
          code_index = self.current_code_index()
          raise SemanticError(f'Double declaration for variable "{lexeme}" at line {code_index}')
        
        self.declared_vars.append(self.lexeme_pairs[self.pos])

      self.advance()

  def validate_variable_usage(self):
    self.pos = 0
    in_code_block = False

    while self.pos < len(self.lexeme_pairs):
      # Identify the start of the code block
      if self.check_token(TokenEnum.INICIO):
        in_code_block = True
      elif in_code_block and self.check_token(TokenEnum.ID):
        lexeme = self.current_lexeme()

        # Check declaration
        if not self.is_variable_declared(lexeme):
          code_index = self.current_code_index()
          raise SemanticError(f'Undeclared variable "{lexeme}" used at line {code_index}.')

      self.advance()
  
  def is_variable_declared(self, lexeme) -> bool:
    return any(var['lexeme'] == lexeme for var in self.declared_vars)
