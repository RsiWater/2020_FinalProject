import sqlite3

connection = sqlite3.connect('test.db')
connection2 = sqlite3.connect('test.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE PERSON3
                (ID INT PRIMARY KEY NOT NULL);''')
connection.commit()
cursor = connection2.cursor()
cursor.execute('''CREATE TABLE PERSON2
                (ID INT PRIMARY KEY NOT NULL);''')
connection2.commit()
connection.close()
connection2.close()
print(connection)
print(connection2)