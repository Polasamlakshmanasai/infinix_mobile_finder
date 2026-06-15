import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("auth.db")

# Create cursor
cursor = conn.cursor()

# Delete old users table if it exists
cursor.execute("""
DROP TABLE IF EXISTS users
""")

# Create new users table
cursor.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database and users table created successfully!")