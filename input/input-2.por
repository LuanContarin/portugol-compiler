algoritmo "verifica_entrada_festa"
var
  idade, maioridade: inteiro
inicio
  maioridade <- 18

  escreva("Digite sua idade: ")
  leia(idade)

  se (idade < maioridade) então
    escreva("Entrada negada. Menor de idade sem autorização.")
  senão
    escreva("Entrada permitida. Boa festa!")
  fimse
fimalgoritmo
