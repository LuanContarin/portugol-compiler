import analyzers.lexical_analyzer as lexical_analyzer
import analyzers.syntax_analyzer as syntax_analyzer

INPUT_FILE_NAME = 'input-2.por'

def main():
  try:
    # Lexer
    lexeme_pairs = lexical_analyzer.compile(INPUT_FILE_NAME)

    # Syntax
    syntax_analyzer.compile(lexeme_pairs)

  except Exception as e:
    print(f'[COMPILATION ERROR]:\n\t{e}')


if __name__ == "__main__":
  main()