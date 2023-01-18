import sqlite3

conn = sqlite3.connect('myDatabse.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Register(
fname varshar(100),
lname varshar(100),
card varshar(100),
psw varshar(100))""")
conn.commit()