from typing import Dict, List

from utils.token_enum import TokenEnum

class Parser:
  def __init__(self, tokens: List[Dict[str, str]]):
    self.tokens = tokens
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['token']
    
    return TokenEnum.END_OF_FILE
  
  def current_lexeme(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['lexeme']
    
    return ' '
  
  def current_code_index(self) -> str:
    if self.pos < len(self.tokens):
      return self.tokens[self.pos]['code_index']
    elif self.tokens:
      return self.tokens[-1]['']['code_index']
    
    return 'unknown'

  def expect_token(self, expected: TokenEnum):
    if self.current_token() == expected.name:
      self.pos += 1
      return
    
    lexeme = self.current_lexeme()
    code_index = self.current_code_index()
    raise SyntaxError(f'Expected "{expected.value}", got "{lexeme}" at line {code_index}')
  
  def check_token(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name
  
  def check_token_any(self, expected: List[TokenEnum]) -> bool:
    return any(self.current_token() == t.name for t in expected)

  def parse(self):
    self.expect_token(TokenEnum.ALGORITMO)
    self.expect_token(TokenEnum.STRING)

    if self.check_token(TokenEnum.VAR):
      self.grammar_variable_block()

    self.expect_token(TokenEnum.INICIO)

    while not self.check_token_any([TokenEnum.FIMALGORITMO, TokenEnum.END_OF_FILE]):
      self.statement()

    self.expect_token(TokenEnum.FIMALGORITMO)

  def statement(self):
    if self.check_token(TokenEnum.ID):
      self.grammar_var_assignment()
    elif self.check_token(TokenEnum.ESCREVA):
      self.grammar_command_escreva()
    elif self.check_token(TokenEnum.LEIA):
      self.grammar_command_leia()
    elif self.check_token(TokenEnum.SE):
      self.grammar_command_se()
    elif self.check_token(TokenEnum.PARA):
      self.grammar_command_para()
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Unexpected "{lexeme}" at line {code_index}')

  # ----------------
  # Grammars
  # ----------------
  def grammar_variable_block(self):
    self.expect_token(TokenEnum.VAR)

    while self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)

      # Optional IDs separated by commas
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)

      self.expect_token(TokenEnum.COLON)
      self.expect_token(TokenEnum.TIPO)

  def grammar_var_assignment(self):
    self.expect_token(TokenEnum.ID)
    self.expect_token(TokenEnum.ATR)
    self.grammar_arithmetic_expression()

  def grammar_command_escreva(self):
    self.expect_token(TokenEnum.ESCREVA)
    self.expect_token(TokenEnum.PARAB)

    # Terms supported by escreva
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.STRING):
      self.expect_token(TokenEnum.STRING)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Unexpected "{lexeme}" in escreva at line {code_index}')

    self.expect_token(TokenEnum.PARFE)

  def grammar_command_leia(self):
    self.expect_token(TokenEnum.LEIA)
    self.expect_token(TokenEnum.PARAB)

    # Terms supported by leia
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntaxError(f'Unexpected "{lexeme}" in leia at line {code_index}')

    self.expect_token(TokenEnum.PARFE)
  
  def grammar_command_se(self):
    self.expect_token(TokenEnum.SE)
    self.grammar_logic_expression()

    self.expect_token(TokenEnum.ENTAO)
    while not self.check_token_any([TokenEnum.SENAO, TokenEnum.FIMSE]):
      self.statement()
    
    if self.check_token(TokenEnum.SENAO):
      self.expect_token(TokenEnum.SENAO)
      while not self.check_token(TokenEnum.FIMSE):
        self.statement()

    self.expect_token(TokenEnum.FIMSE)

  def grammar_command_para(self):
    self.expect_token(TokenEnum.PARA)
    self.expect_token(TokenEnum.ID)
    self.expect_token(TokenEnum.ATE)
    self.expect_token(TokenEnum.NUMINT)

    # Optional "passo"
    if self.check_token(TokenEnum.PASSO):
      self.expect_token(TokenEnum.PASSO)
      self.expect_token(TokenEnum.NUMINT)

    while not self.check_token(TokenEnum.FIMPARA):
      self.statement()

    self.expect_token(TokenEnum.FIMPARA)

  #
  # Fundamental
  #
  def grammar_arithmetic_expression(self):
    self.grammar_arithmetic_term()
    
    while self.check_token_any([TokenEnum.OPMAIS, TokenEnum.OPMENOS, TokenEnum.OPMULTI, TokenEnum.OPDIVI]):
      self.pos += 1
      self.grammar_arithmetic_term()

  def grammar_arithmetic_term(self):
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_arithmetic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      code_index = self.current_code_index()
      raise SyntaxError(f'Expected identifier or value in expression at line {code_index}')

  def grammar_logic_expression(self):
    self.grammar_logic_comparison()
    while self.check_token_any([TokenEnum.E, TokenEnum.OU]):
      self.pos += 1
      self.grammar_logic_comparison()

  def grammar_logic_comparison(self):
    if self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_logic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      self.grammar_logic_operand()
      if self.check_token_any([
        TokenEnum.LOGIGUAL, TokenEnum.LOGDIFF,
        TokenEnum.LOGMENOR, TokenEnum.LOGMENORIGUAL,
        TokenEnum.LOGMAIOR, TokenEnum.LOGMAIORIGUAL
      ]):
        self.pos += 1
        self.grammar_logic_operand()
      else:
        code_index = self.current_code_index()
        raise SyntaxError(f'Missing comparison operator in logical expression at line {code_index}')

  def grammar_logic_operand(self):
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.STRING):
      self.expect_token(TokenEnum.STRING)
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_logic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      code_index = self.current_code_index()
      raise SyntaxError(f'Expected operand in logical expression at line {code_index}')
