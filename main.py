import pandas as pd
import psycopg2
import sys, getopt


if __name__ == '__main__':
    
    argv = sys.argv[1:]
    try: 
        opts, args = getopt.getopt(argv, "d:s:",["sgbd =", "schema ="]) 
    except: 
        print("Parâmetros inválidos. Informe o sgbd e o schema desejados. Ex.: --sgbd postgres --schema vendas") 