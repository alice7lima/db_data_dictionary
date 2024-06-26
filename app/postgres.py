from decouple import config
import psycopg2
import pandas as pd

DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')

class PostgresDict():
    def __init__(self, schema):
        self.conn = None
        self.schema = schema
        
    def create_connection(self):
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD)
        except psycopg2.OperationalError as e:
            print('Não foi possível estabelecer conexão com o banco. Verifique se as variáveis de conexão estão corretas.')
            exit()
            

    def get_tables_names(self):

        cur = self.conn.cursor()
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema= %s 
        AND table_type = 'BASE TABLE';
        """

        cur.execute(query, (self.schema,))

        result = cur.fetchall()

        table_list = [registro[0] for registro in result]

        cur.close()
        return table_list

    def get_table_comment(self,table_name):

        cur = self.conn.cursor()
        query = """
        SELECT pg_catalog.obj_description(pgc.oid, 'pg_class') AS table_comment
        FROM information_schema.tables t
        INNER JOIN pg_catalog.pg_class pgc
        ON t.table_name = pgc.relname 
        WHERE t.table_name = %s
        AND t.table_schema= %s;
        """

        cur.execute(query, (table_name, self.schema,))
        comment = str(cur.fetchone()[0]).strip()

        if comment == 'None':
            comment = ''

        cur.close()
        return comment

    def get_table_constraints(self, table_name):
        cur = self.conn.cursor()

        query_constraints = """
        SELECT kc.column_name, cons.contype  
        FROM information_schema.key_column_usage kc
        inner join pg_catalog.pg_constraint cons on cons.conname = kc.constraint_name 
        WHERE kc.table_schema  = %s
        and kc.table_name = %s
        """

        cur.execute(query_constraints, (self.schema, table_name))

        constraints = cur.fetchall()

        return dict(constraints)


    def get_columns_info(self, table_name):

        table_constraints = self.get_table_constraints(table_name=table_name) 
        cur = self.conn.cursor()

        query = """
        WITH descricoes as (
            SELECT *  FROM pg_catalog.pg_description d
            INNER JOIN pg_catalog.pg_class pgc on pgc."oid" = d.objoid 
            WHERE relname = %s AND relnamespace = (
            SELECT oid FROM pg_catalog.pg_namespace WHERE nspname = %s)
        )

        SELECT c.column_name, c.is_nullable,c.data_type,t2.description FROM information_schema.columns c
        LEFT JOIN descricoes t2 on t2.objsubid = c.ordinal_position 
        WHERE c.table_name  = %s
        AND c.table_schema = %s
        ORDER BY c.ordinal_position 
        """

        cur.execute(query, (table_name, self.schema, table_name, self.schema))
        cols_infos = cur.fetchall()

        cols_infos = [list(register) for register in cols_infos]

        for idx, col in enumerate(cols_infos):
            if col[0] in table_constraints.keys():
                cols_infos[idx].append(table_constraints[col[0]])

            else:
                cols_infos[idx].append('')

        return cols_infos

    def pg_data_dictionary(self):
        
        #cur = self.conn.cursor()

        tables_comments = {}
        tables = self.get_tables_names()


        for table in tables:
            tables_comments[table] = self.get_table_comment(table_name=table)

        df = pd.DataFrame(columns=['Tabela', 'Descrição', 'Coluna', 'Constraint', 'Tipo', 'Null','Comentário'])

        for table in tables_comments.keys():
            colunas = self.get_columns_info(table_name=table)
            for idx, c in enumerate(colunas):
                registro = {'Tabela': table, 'Descrição': tables_comments[table], 'Coluna': c[0], 
                        'Constraint': c[4],'Tipo': c[2], 'Null': c[1], 'Comentário': c[3]}
                
                if idx != 0:
                    registro['Descrição'] = ''
                

                df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)

            
        return df
