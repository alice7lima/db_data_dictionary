from app import PostgresDict
import pandas as pd
import sys, getopt


argv = sys.argv[1:]

try: 
    opts, args = getopt.getopt(argv, "d:s:",["sgbd=", "schema="]) 
    opts = dict(opts)

    if opts['--sgbd'] == 'postgres':
        builder = PostgresDict(schema=opts['--schema'])
        dicionario = builder.pg_data_dictionary()

        dicionario.to_excel('test_output.xlsx', index=False)

    else:
        print("Ainda não há implementação para este SGBD. Por favor aguarde.")

except: 
    print("Parâmetros inválidos. Informe o sgbd e o schema desejados. Ex.: --sgbd postgres --schema vendas") 