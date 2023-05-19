# Geração de Branches Git para Arquivo de Parâmetros

Este script gera múltiplas branches no Git para cada versão de um arquivo `params.yaml`, representando intervalos de um ano nos dados de treinamento. Cada branch é criada com base em uma data de início e fim fornecida, atualizando o arquivo `params.yaml` correspondente para cada branch.

## Requisitos

- Python 3.x
- Git
- Bibliotecas Python: `datetime`, `subprocess`, `yaml`, `logging`, `pathlib`

## Configuração

Antes de executar o script, certifique-se de que o arquivo `params.yaml` está localizado no mesmo diretório do script e verifique as configurações a seguir:

- `params_file`: O nome do arquivo de parâmetros.
- `start_date`: A data de início para a primeira branch.
- `num_years`: O número de branches a serem criadas.

## Execução

Execute o script fornecendo os valores adequados para as configurações mencionadas acima. O script irá gerar as branches correspondentes para cada ano no intervalo especificado.

Exemplo de uso:

```shell
python gerador_branches.py
```

## Funcionalidades
- `create_git_branch(params_file, start_date, end_date)`: Cria uma branch no Git para um determinado arquivo de parâmetros e intervalo de datas.
- `update_params_file(params_file, start_date, end_date)`: Atualiza o arquivo de parâmetros com as datas fornecidas.
- `generate_git_branches(params_file, start_date, num_years)`: Cria uma branch para cada ano no intervalo especificado.

## Observações
Certifique-se de que o Git está instalado corretamente e configurado para uso no ambiente em que o script será executado.

Certifique-se também de ter as bibliotecas Python mencionadas instaladas no ambiente em que o script será executado.

**Nota:** Este script foi desenvolvido e testado em um ambiente Linux.

Este README.md fornece uma descrição geral do script, incluindo informações sobre configurações, requisitos, instruções de execução, funcionalidades e observações importantes. Ele também inclui exemplos de uso e observações finais sobre a origem do código.
