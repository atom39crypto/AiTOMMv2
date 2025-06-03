import sqlite3
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MessageEntity:
    def __init__(self, role: str, content: str):
        self.role = role  
        self.content = content


def load_memory(username: str) -> list[MessageEntity]:

    table_name = username
    db_path = 'Core/Memo/memory.db'
    
    # Check if the database exists.
    if not os.path.exists(db_path):
        print("Database not found.")
        return []
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if the user's table exists.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if not cursor.fetchone():
        print(f"No conversation found for user '{username}'.")
        conn.close()
        return []
    
    # Fetch all messages (ordered by insertion order).
    cursor.execute(f'SELECT role, content FROM "{table_name}" ORDER BY id ASC')
    rows = cursor.fetchall()
    conn.close()
    
    return [MessageEntity(row["role"], row["content"]) for row in rows]

def retrieve_similar_memory(user_input: str, entities: list[MessageEntity], top_n=3):
    """
    Retrieve conversation pairs (user query and assistant response) that are most similar
    to the user_input using TF-IDF and cosine similarity.
    """
    try:
        memory_contents = [entity.content for entity in entities]
        
        # Include the user input in vectorization for comparison.
        vectorizer = TfidfVectorizer().fit(memory_contents + [user_input])
        memory_vectors = vectorizer.transform(memory_contents)
        user_vector = vectorizer.transform([user_input])
        
        similarities = cosine_similarity(user_vector, memory_vectors).flatten()
        similar_indices = similarities.argsort()[-top_n:][::-1]  # Get indices of top similar messages
        
        similar_messages = [entities[i] for i in similar_indices]
        
        pairs = []
        # Try to pair a user message with the corresponding assistant reply.
        for msg in similar_messages:
            if msg.role == "user":
                idx = entities.index(msg) + 1  # Next message assumed to be the assistant's response
                if idx < len(entities) and entities[idx].role == "assistant":
                    pairs.append((msg, entities[idx]))
            elif msg.role == "assistant":
                idx = entities.index(msg) - 1  # Previous message assumed to be the user's query
                if idx >= 0 and entities[idx].role == "user":
                    pairs.append((entities[idx], msg))
        
        result = []
        for user_msg, assistant_msg in pairs:
            result.append({"role": user_msg.role, "content": user_msg.content})
            result.append({"role": assistant_msg.role, "content": assistant_msg.content})
        
    
        return result
    except Exception as e:
        print("no related memory found")
        return []

       
def relamemo(username: str, user_input: str):
    try:
        print("<=- Retrieving the relative memory -=>")
        entities = load_memory(username)
        similar_pairs = retrieve_similar_memory(user_input, entities, top_n=3)
        return similar_pairs
    except Exception:
        return "NO relative memory."

if __name__ == "__main__":
    username = input("Enter your username: ").strip()
    user_input = input("Enter your query: ").strip()
    similar_memory = relamemo(username, user_input)
    print("\nSimilar memory pairs:")
    print(similar_memory)
