import sqlite3
import os

# Define the path to the SQLite database.
db_path = 'Core/Memo/memory.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def get_connection():
    return sqlite3.connect(db_path)

def sanitize_table_name(username):

    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    safe_username = "".join(c for c in username if c in allowed_chars)
    if not safe_username:
        safe_username = "default_user"
    if safe_username[0].isdigit():
        safe_username = "_" + safe_username
    return safe_username

def create_table_if_not_exists(username):

    table_name = sanitize_table_name(username)
    conn = get_connection()
    cursor = conn.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

def load_memory(username, limit=6):
    """
    Load the most recent conversation messages for the user.
    Retrieves the last `limit` rows (messages) from the user’s table.
    Returns the rows in chronological order as dictionaries without the timestamp.
    """
    table_name = sanitize_table_name(username)
    # Ensure the table exists.
    create_table_if_not_exists(username)
    conn = get_connection()
    # Set the row factory to sqlite3.Row to retrieve dictionary-like rows.
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Query only the role and content columns (exclude the timestamp).
    query = f'SELECT role, content FROM "{table_name}" ORDER BY id DESC LIMIT ?'
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    # Convert each row to a dictionary and reverse to display in chronological order.
    return [dict(row) for row in rows][::-1]


if __name__ == "__main__":
    # Prompt the user for their username.
    username = input("Enter your username: ").strip()
    if not username:
        print("Username cannot be empty.")
    else:
        # Load the last 6 messages for this user.
        result = load_memory(username)
        print(f"\nLoaded conversation memory for '{username}':")
        for row in result:
            print(row)  # Each row is a dict with 'role' and 'content'
        
        # Example conversation to save.
        user_input = f"I am {username}"
        assistant_response = f"halo {username}"
