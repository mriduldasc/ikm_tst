import pyodbc
import psycopg2


sql_server_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_sql_server;DATABASE=your_database;UID=your_username;PWD=your_password')
sql_server_cursor = sql_server_conn.cursor()

postgres_conn = psycopg2.connect(host='localhost', database='master', user='admin', password='admin')
postgres_cursor = postgres_conn.cursor()

sql_server_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA = 'dbo'")
sql_server_tables = [row[0] for row in sql_server_cursor.fetchall()]


postgres_cursor.execute("SELECT table_name  FROM information_schema.tables WHERE table_schema = 'public'")
postgres_tables = [row[0] for row in postgres_cursor.fetchall()]

tables_to_skip = set(sql_server_tables) & set(postgres_tables)

for table_name in sql_server_tables:
    if table_name in tables_to_skip:
        print(f"Skipping table '{table_name}' as it already exists in PostgreSQL.")
        continue


sql_server_cursor.close()
sql_server_conn.close()

postgres_cursor.close()
postgres_conn.close()
