import pyodbc
import psycopg2


sql_server_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_sql_server;DATABASE=your_database;UID=your_username;PWD=your_password')
sql_server_cursor = sql_server_conn.cursor()


postgres_conn = psycopg2.connect(host='localhost', database='master', user='admin', password='admin')
postgres_cursor = postgres_conn.cursor()

table_name = 'customers'


sql_server_cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'dbo'")
sql_server_columns = {row[0]: row[1] for row in sql_server_cursor.fetchall()}


postgres_cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
postgres_columns = {row[0]: row[1] for row in postgres_cursor.fetchall()}


columns_to_add_defaults = set(sql_server_columns.keys()) - set(postgres_columns.keys())


default_values = {
    'int': 0,  
    'nvarchar': '',  
   
}


if columns_to_add_defaults:
    for column_name in columns_to_add_defaults:
        data_type = sql_server_columns[column_name]
        default_value = default_values.get(data_type, None)

        if default_value is not None:
            print(f"Inserting default value '{default_value}' into column '{column_name}' for table '{table_name}' in PostgreSQL.")
            postgres_cursor.execute(f"UPDATE {table_name} SET {column_name} = {default_value} WHERE {column_name} IS NULL")


postgres_conn.commit()

sql_server_cursor.close()
sql_server_conn.close()

postgres_cursor.close()
postgres_conn.close()

