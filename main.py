from app import PostgresDict
import sys, getopt


argv = sys.argv[1:]

try: 
    opts, args = getopt.getopt(argv, "d:s:",["sgbd=", "schema="]) 
    opts = dict(opts)

except: 
    print("Parâmetros inválidos. Informe o sgbd e o schema desejados. Ex.: --sgbd postgres --schema vendas")
    exit() 

if opts['--sgbd'] == 'postgres':


    builder = PostgresDict(schema=opts['--schema'])
    builder.create_connection()

    dicionario = builder.pg_data_dictionary()

    dicionario.to_excel(f'sc_{opts['--schema']}_dicionario.xlsx', index=False)

else:
    print("Ainda não há implementação para este SGBD. Por favor aguarde.")