import sqlite3
import json

# Path to the database file
db_path = "local_memory.db"

# SQL query to create a table for a specific user if it doesn't exist
def create_user_table(username):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS '{username}' (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        conversation_history TEXT
    );
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(create_table_query)
            print(f"Table for user '{username}' created.")
    except sqlite3.Error as e:
        print(f"Error creating table for user '{username}': {e}")

# Function to add a new conversation for a specific user
def add_conversation(username, conversation_history):
    try:
        create_user_table(username)  # Ensure the user's table exists
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
            INSERT INTO '{username}' (username, conversation_history)
            VALUES (?, ?)
            """, (username, json.dumps(conversation_history)))  # Store conversation as JSON
            conn.commit()
            print(f"Conversation added for user '{username}'.")
    except sqlite3.Error as e:
        print(f"Error adding conversation for user '{username}': {e}")

# Function to load memory (conversation history) for a specific user
def load_memory(query):
    print(f"<=- Load Memory ; Query : {query} -=>")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Execute the provided query
            cursor.execute(query)
            rows = cursor.fetchall()

            results = []
            for row in rows:
                try:
                    # Assuming conversation_history is stored as a JSON string
                    conversation_history = json.loads(row[0])
                    results.append(conversation_history)
                except (json.JSONDecodeError, TypeError, IndexError):
                    # If JSON decoding fails, append the raw row
                    results.append(row)

            return results

    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

# Example usage: Adding a new conversation for 'shounak'
if __name__ == "__main__":
    new_conversation = {
        "messages": [
            {"user": "shounak", "message": "what us the best bevarage ?"},
            {"user": "assistant", "message": "It is the coffee"}
        ]
    }
    add_conversation("shounak", new_conversation)

    # Example usage of loading memory for 'shounak' (ensure correct table exists)
    query = "SELECT conversation_history FROM 'shounak' WHERE username='shounak' LIMIT 5;"
    results = load_memory(query)
    print("Memory Loaded:", results)
