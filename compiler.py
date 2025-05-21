import analyzers.lexical_analyzer as lexical_analyzer
import analyzers.syntax_analyzer as syntax_analyzer
import analyzers.semantic_analyzer as semantic_analyzer

INPUT_FILE_NAME = 'TESTE_SEM_ERRO.POR'

def main():
  try:
    # Lexer
    lexeme_pairs = lexical_analyzer.compile(INPUT_FILE_NAME)

    # Parser
    parser = syntax_analyzer.Parser(lexeme_pairs)
    parser.parse()
    print('✅ Syntax is valid.')

    # Semantic Analyzer
    semantic = semantic_analyzer.SemanticAnalyzer(lexeme_pairs)
    semantic.validate()
    print('✅ Semantic is valid.')

    print('[COMPILED SUCCESSFULLY]')

  except Exception as e:
    print(f'[COMPILATION ERROR]:\n\t{e}')


if __name__ == "__main__":
  main()