from utils import postgres
import pandas as pd
import sys, getopt


argv = sys.argv[1:]

try: 
    opts, args = getopt.getopt(argv, "d:s:",["sgbd=", "schema="]) 
    opts = dict(opts)
    dicionario = postgres.build_data_dictionary(schema=opts['--schema'])
    dicionario.to_excel('saida.xlsx', index=False)
except: 
    print("Parâmetros inválidos. Informe o sgbd e o schema desejados. Ex.: --sgbd postgres --schema vendas") 