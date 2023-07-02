import sqlite3
conn = sqlite3.connect("hospital.db")
print("opened database successfully")


conn.execute("CREATE TABLE predict (id INTEGER PRIMARY KEY AUTOINCREMENT,uname varchar,uage varchar,ugender varchar,udate varchar, uddate varchar,udesease varchar,ulocation varchar,uzipcode varchar)")
conn.execute("CREATE TABLE signup (uname varchar,uphone varchar,username varchar,upassword varchar)")

print("table created successfully")
conn.close()
