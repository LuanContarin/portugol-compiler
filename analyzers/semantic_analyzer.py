from typing import Dict, List

from utils.token_enum import TokenEnum

class SemanticError(Exception):
  pass

class SemanticAnalyzer:
  def __init__(self, lexemePairs: List[Dict[str, str]]):
    self.lexeme_pairs = lexemePairs
    self.declared_vars = []
    self.assigned_vars = []
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
    self.validate_variable_usage()

  # ----------------
  # Validations
  # ----------------
  def validate_variable_usage(self):
    self.pos = 0
    while not self.check_token(TokenEnum.END_OF_FILE):
      # Add declarations
      if self.check_token(TokenEnum.TIPO):
        self.advance()
        self.advance()

        var_name = self.current_lexeme()

        if self.is_variable_declared(var_name):
          code_index = self.current_code_index()
          raise SemanticError(f'Double declaration for variable "{var_name}" at line {code_index}')

        self.declared_vars.append(self.lexeme_pairs[self.pos])
      # Add variable assignment via leia()
      elif self.check_token(TokenEnum.LEIA):
        self.advance()
        self.advance()

        var_name = self.current_lexeme()

        if not self.is_variable_declared(var_name):
          code_index = self.current_code_index()
          raise SemanticError(f'Undeclared variable "{var_name}" used at line {code_index}.')
        
        if not self.is_variable_assigned(var_name):
          self.assigned_vars.append(self.lexeme_pairs[self.pos])
      # Check variable usage
      elif self.check_token(TokenEnum.ID):
        var_name = self.current_lexeme()

        # Check if assignment and supply assigned vars
        next_token = self.lexeme_pairs[self.pos + 1]['token'] if self.pos + 1 < len(self.lexeme_pairs) else None
        if next_token == TokenEnum.ATR.name and not self.is_variable_assigned(var_name):
          if not self.is_variable_declared(var_name):
            code_index = self.current_code_index()
            raise SemanticError(f'Undeclared variable "{var_name}" used at line {code_index}.')

          self.assigned_vars.append(self.lexeme_pairs[self.pos])
          self.advance()
          continue
        
        if not self.is_variable_declared(var_name):
          code_index = self.current_code_index()
          raise SemanticError(f'Undeclared variable "{var_name}" used at line {code_index}.')
        
        if not self.is_variable_assigned(var_name):
          code_index = self.current_code_index()
          raise SemanticError(f'Unassigned variable "{var_name}" used at line {code_index}.')

      self.advance()
  
  def is_variable_declared(self, lexeme) -> bool:
    return any(var['lexeme'] == lexeme for var in self.declared_vars)

  def is_variable_assigned(self, lexeme) -> bool:
    return any(var['lexeme'] == lexeme for var in self.assigned_vars)
