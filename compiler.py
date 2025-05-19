import analyzers.lexical_analyzer as lexical_analyzer
import analyzers.syntax_analyzer as syntax_analyzer

INPUT_FILE_NAME = 'input-2.por'

def main():
  try:
    # Lexer
    lexeme_pairs = lexical_analyzer.compile(INPUT_FILE_NAME)

    # Parser
    parser = syntax_analyzer.Parser(lexeme_pairs)
    parser.parse()
    print('✅ Syntax is valid.')

  except Exception as e:
    print(f'[COMPILATION ERROR]:\n\t{e}')


if __name__ == "__main__":
  main()