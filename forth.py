import pyodbc
import psycopg2
import logging


logging.basicConfig(filename='migration.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


sql_server_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_sql_server;DATABASE=your_database;UID=your_username;PWD=your_password')
sql_server_cursor = sql_server_conn.cursor()


postgres_conn = psycopg2.connect(host='localhost', database='master', user='admin', password='admin')
postgres_cursor = postgres_conn.cursor()

table_name = 'customers'

try:
 
    sql_server_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sql_server_cursor.fetchall()


    for row in rows:
        postgres_cursor.execute(f"INSERT INTO {table_name} (column1, column2, column3) VALUES (%s, %s, %s)", row)  # Replace column1, column2, column3 with actual column names


    postgres_conn.commit()

except Exception as e:

    logging.error(f"An error occurred during the migration of table '{table_name}': {str(e)}")


sql_server_cursor.close()
sql_server_conn.close()

postgres_cursor.close()
postgres_conn.close()
