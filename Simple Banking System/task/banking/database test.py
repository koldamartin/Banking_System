import sqlite3
conn = sqlite3.connect('card.s3db') #create a connection object that represents the database
cur = conn.cursor() #create a cursor object
cur.execute("DROP TABLE IF EXISTS card")
cur.execute("CREATE TABLE IF NOT EXISTS card (id INT,number TEXT,pin TEXT,balance INT DEFAULT 0)")
cur.execute("INSERT INTO card (id, number, pin) VALUES (01, '91684404', '3080')")
#conn.commit()
result = cur.execute(("SELECT number FROM card"))
print(result.fetchall())

