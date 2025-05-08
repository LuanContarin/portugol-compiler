from typing import NamedTuple

class TokenMatch(NamedTuple):
  start: int
  end: int
  replacement: str
