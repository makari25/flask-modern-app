import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insert some sample data
cur.execute("INSERT INTO tasks (content, priority) VALUES (?, ?)",
            ('Finish Flask Tutorial', 'High')
            )

cur.execute("INSERT INTO tasks (content, priority) VALUES (?, ?)",
            ('Deploy to Production', 'Medium')
            )

connection.commit()
connection.close()