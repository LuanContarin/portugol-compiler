# portugol-compiler

A portugol compiler made using Python

# TODO:

- Criar a tabela de tokens p/ analise lexica
  <br>

  ```
    ✅ Recommended Token Matching Order:
    Here's a safe and logical default matching priority for most lexical analyzers:

    String Literals (e.g., "Texto com espaços")

    Must be matched first so inner content isn't tokenized (e.g., keywords or operators inside strings).

    Multi-character Operators (e.g., <=, >=, <-, <>)

    Must come before single-character operators like < or =, to avoid early termination.

    Single-character Operators & Punctuation (e.g., +, -, =, /, (, ))

    Keywords / Reserved Words (e.g., escreva, leia, se, fim_se)

    Should be matched before identifiers, because they look like identifiers.

    Numeric Constants (e.g., 10, 3)

    Often matched as a separate category like NUMINT.

    Identifiers (e.g., idade1, media_idade)

    Matched after keywords so reserved words aren't mistaken as identifiers.

    Unknown / Error Tokens

    Anything else not matching a valid pattern is typically marked as UNKNOWN or causes an error.
  ```

- ...
