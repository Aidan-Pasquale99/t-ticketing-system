import sqlite3
import datetime

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

cur.execute("INSERT INTO tickets (ticket_name, ticket_description, created_date, due_date, status, department, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Test Ticket',  'Test description', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '2023-05-01 10:00:00', 'Pending', 'Product', 'Development')
            )

conn.commit()
conn.close()