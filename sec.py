import pyodbc
import psycopg2


sql_server_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_sql_server;DATABASE=your_database;UID=your_username;PWD=your_password')
sql_server_cursor = sql_server_conn.cursor()


postgres_conn = psycopg2.connect(host='localhost', database='master', user='admin', password='admin')
postgres_cursor = postgres_conn.cursor()

table_name = 'Customer'


sql_server_cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}' AND TABLE_SCHEMA = 'dbo'")
sql_server_columns = [row[0] for row in sql_server_cursor.fetchall()]


postgres_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
postgres_columns = [row[0] for row in postgres_cursor.fetchall()]


columns_to_skip = set(sql_server_columns) - set(postgres_columns)

for column_name in sql_server_columns:
    if column_name in columns_to_skip:
        print(f"Skipping column '{column_name}' in table '{table_name}' as it is not present in PostgreSQL.")
        continue


sql_server_cursor.close()
sql_server_conn.close()

postgres_cursor.close()
postgres_conn.close()