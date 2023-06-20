import pyodbc
server = 'localhost'  # Replace with your SQL Server instance name
database = 'master'  # Replace with your database name
username = ''  # Replace with your username
password = ''  # Replace with your password
tcon="True"

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
conn = pyodbc.connect(driver='{SQL Server}', host=server, database=database,
                      trusted_connection=tcon, user=username, password=password)
cursor = conn.cursor()

cursor.execute('SELECT * FROM Customers')

rows = cursor.fetchall()
for row in rows:
    print("rr=",row)

print("asd")
cursor.close()
conn.close()
print("ovr")
