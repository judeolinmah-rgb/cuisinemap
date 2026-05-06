import sqlite3
conn = sqlite3.connect('cuisinemap.db')
try:
    conn.execute('ALTER TABLE taste_history ADD COLUMN hit_meals TEXT DEFAULT "{}"')
    conn.commit()
    print('Column added successfully')
except Exception as e:
    print('Already exists or error:', e)
conn.close()