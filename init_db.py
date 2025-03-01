import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# Create Customers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    uen TEXT,
    year_end TEXT,
    date_of_incorporation TEXT,
    person_in_charge TEXT,
    contact_number TEXT
);
""")

# Save changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully!")
