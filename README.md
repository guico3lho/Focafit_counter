# Focafit Counter

## Esse repositório contém o código para o Focafit Counter: uma automação para contar o número de pontos que cada núcleo da CJR fez semanalmente fazendo exercícios!

## Visão geral do projeto
- A pasta `assets` contém os arquivos de entrada e saída do projeto
- A pasta `src` contém o código que o Focafit Counter usa para funcionar
- O arquivo `requirements.txt` contém as dependências do projeto
- [OPCIONAL] A pasta `.runAndDebugOnPyCharm` contém configurações para executar o projeto no Pycharm

## O projeto foi feito usando:
- PyCharm IDE
- Anaconda
- Python 3.10.9
- Windows 10+
- Todas as bibliotecas usadas estão listadas no arquivo `requirements.txt`

## Configurando o ambiente
- Vá no grupo do Whatsapp "Focafit" e exporte a conversa em formato txt
- Clone o repositório Focafit_counter
- Dentro da pasta `Focafit_counter`:
  - Instale as dependências usando `pip install -r requirements.txt`;
  - Adicione o arquivo txt exportado do grupo "Focafit" do Whatsapp na pasta `assets/input`.


## Parâmetros
- Esse projeto usa a biblioteca `argparse`
- Atualmente, existem 3 argumentos:
  - `"-i"` para especificar o arquivo de entrada (formato: path, tipo: str)
  - `"-o"` para especificar o arquivo de saída (formato: path, tipo: str)
  - `"-d"` colocar o último dia que a contagem será levada em consideração. O bot irá levar em consideração esse dia e os 6 anteriores (formato: "dd/mm/yyyy", tipo: str)

## Exemplo da contagem de pontos de uma semana arbitrária (08/05/2023 a 14/05/2023)
- Dentro da pasta `Focafit_counter`:
  - Rode `python -m src.counter -i "./assets/input/chat_example.txt" -o "./assets/output" -d "14/05/2023"` para rodar um exemplo do Focafit_counter!
  - O argumento -d "14/05/2023" foi considerado pois é o último dia da semana que queremos contar os pontos
  - O resultado pode ser checado dentro da pasta `./assets/output`
  - O resultado esperado é:
```
🦾 FOCA FIT SEMANAL - 08/05 A 14/05 🦾 
Gerado por: Focafit_counter 😎 

💜💙🖤 RANKING POR NÚCLEO 💚🧡💛 

1ª BOPE: 40
2ª NOE: 6
3ª NUT: 4
4ª NDP: 2


🏆 RANKING POR PESSOA 🏆

1º Chico: 4
2º Zeca: 2

```
