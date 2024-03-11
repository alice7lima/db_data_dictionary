# Gerador de dicionário de dados

![Diagrama](/diagram.png "Diagrama")


Este projeto é a implementação em python de um gerador de dicionário de dados. O script extrai as informações das tabelas de um schema de bancos de dados e salva as informações em arquivo excel (xlsx). 

\*Por enquanto o projeto está implementado apenas para SGBD PostgreSQL.

O dicionário de dados contém as seguintes informações:

- **Tabela**: Nome da tabela
- **Descrição**: Descrição da tabela
- **Coluna**: Nome da coluna
- **Constraint**: Indica restrições da coluna (primary key, foreign key, unique, check)
- **Tipo**: Tipo de dado da coluna
- **Null**: Indica se a coluna aceita valores nulos ou não
- **Comentário**: Descrição da coluna

# Como executar

1. Configure a versão do python com `pyenv`:

```
pyenv install 3.12
pyenv local 3.12
```

2. Configure o ambiente

2.1 Ambiente virtual e dependências do projeto
```
python -m venv .venv
source .venv/bin/activate

#instale as dependências
pip install -r requirements.txt
```

2.2 Configurando as variáveis de ambiente, primeiro, crie um arquivo .env declarando as variáveis de conexão:

```
DB_HOST = <seu_host>
DB_NAME = <nome_banco>
DB_USER = <nome_usuario>
DB_PASSWORD = <senha_usuario>
``` 

3. Execute o script principal:

```
python main.py --sgbd postgres --schema <nome_do_schema>
```

O dicionário será gerado no arquivo ``sc_<nome_schema>_dicionario.xlsx``.


