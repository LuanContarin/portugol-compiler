# portugol-compiler

A simple Portugol compiler implemented in Python. This project performs lexical, syntactic, and semantic analysis on programs written in a subset of the Portugol language.

## Features

- **Lexical Analysis:** Tokenizes Portugol source code, identifying keywords, operators, identifiers, numbers, and strings.
- **Syntax Analysis:** Checks the structure of the code according to the language grammar.
- **Semantic Analysis:** Validates variable declarations and usage.

## Project Structure

```
.
├── analyzers/
│   ├── lexical_analyzer.py
│   ├── semantic_analyzer.py
│   └── syntax_analyzer.py
├── input/
│   ├── input.por
│   └── input-2.por
├── output/
│   └── lexic_analyzer/
├── utils/
│   ├── file_helper.py
│   ├── token_enum.py
│   └── token_match.py
├── compiler.py
├── README.md
└── LICENSE
```

## Usage

1. Place your Portugol source file in the `input/` directory.
2. Set the `INPUT_FILE_NAME` variable in [`compiler.py`](compiler.py) to your input file name.
3. Run the compiler:

   ```sh
   python compiler.py
   ```

4. Output and intermediate files will be generated in the `output/lexic_analyzer/` directory. The console output status of the compilation (success/errors)

## Example

Sample input files:

- [`input/input.por`](input/input.por)
- [`input/input-2.por`](input/input-2.por)

## Token Matching Order

The lexer matches tokens in the following order:

1. Whitespace/comments (skipped)
2. Strings
3. `<-` (ATR)
4. Keywords (e.g., `para`, `escreva`, `fim_se`)
5. Logical operators (`<=`, `>=`, `<>`, `<`, `>`, `=`)
6. Math operators (`+`, `-`, `*`, `/`)
7. Parentheses
8. Numbers
9. Identifiers
10. Errors

## License

See [LICENSE](LICENSE).
