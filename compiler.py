import analyzers.lexical_analyzer as lexical_analyzer

INPUT_FILE_NAME = 'input-2.por'

def main():
  try:
    # Lexer
    lexical_analyzer.compile(INPUT_FILE_NAME)

    # Syntax

  except Exception as e:
    print(f'[COMPILATION ERROR]:\n\t{e}')


if __name__ == "__main__":
  main()