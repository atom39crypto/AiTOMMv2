import sqlite3
from groq import Groq  # Make sure groq is installed via: pip install groq

# ========== CONFIG ==========
DB_PATH = 'Core/Memo/memory.db'
MAX_WORDS = 100  # Word limit to trigger summarization

# ========== Summarizer ==========
def summarizer(user_data):
    print("Summarizing user data...")
    client = Groq(api_key="enter_your_api_key_here")  # Replace with your actual API key
    try:
        if isinstance(user_data, str):
            user_data = user_data.strip()

        prompt = f"Create a report from the following user data: {user_data}"

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize in 50 words"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=3000,
            top_p=1,
            stream=False
        )

        report = completion.choices[0].message.content
        return report

    except Exception as e:
        return f"An error occurred: {str(e)}"

# ========== Database Utils ==========
def sanitize_table_name(username):
    return ''.join(c for c in username if c.isalnum() or c in ('_', '-')).lower()

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table_if_not_exists(username):
    table_name = sanitize_table_name(username)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ========== Save Conversation ==========
def save_conversation(username, u_resp, a_resp):
    table_name = sanitize_table_name(username)
    create_table_if_not_exists(username)
    conn = get_connection()
    cursor = conn.cursor()

    try:
        insert_query = f'INSERT INTO "{table_name}" (role, content) VALUES (?, ?)'

        # Summarize user message if needed
        if len(u_resp.split()) > MAX_WORDS:
            print("Summarizing user input...")
            summarized = summarizer(u_resp)
            if "error occurred" not in summarized.lower():
                u_resp = "[summarized]\n" + summarized

        # Summarize assistant message if needed
        if len(a_resp.split()) > MAX_WORDS:
            print("Summarizing assistant response...")
            summarized = summarizer(a_resp)
            if "error occurred" not in summarized.lower():
                a_resp = "[summarized]\n" + summarized

        # Insert into DB
        cursor.execute(insert_query, ("user", u_resp))
        cursor.execute(insert_query, ("assistant", a_resp))
        conn.commit()

        print("Conversation saved.")
        return {"status": "success", "message": "Data saved successfully"}

    except sqlite3.Error as e:
        print("Error saving conversation:", e)
        return {"error": str(e)}
    finally:
        conn.close()

# ========== Example Test ==========
if __name__ == "__main__":
    test_user = "Sarbo"
    long_user_input = """Tell me everything you know about the history of computers, from the early days of mechanical machines to modern cloud computing and artificial intelligence..."""
    long_assistant_reply = """**In-Depth Overview of Computer History**  
                            The history of computers is a fascinating journey that began long before the modern digital age. In the early 1800s, **Charles Babbage**, often called the "father of the computer,"
                            designed the **Difference Engine** and the **Analytical Engine**, mechanical devices intended to perform complex calculations. 
                            Although never fully built during his lifetime,
                            Babbage’s concepts laid the foundation for programmable machines. **Ada Lovelace**, a mathematician and Babbage’s collaborator, 
                            is celebrated as the world’s first computer programmer for her work on the Analytical Engine, where she recognized its potential beyond mere calculation.  
                            The late 19th and early 20th centuries saw advancements like **Herman Hollerith’s tabulating machines**, which used punch cards for data processing and played a crucial 
                            role in the U.S. Census. This innovation led to the formation of **IBM**, a key player in early computing.  
                            The mid-1900s marked the transition from mechanical to electronic computing. The **ENIAC (1945)**, one of the first general-purpose electronic computers, used vacuum 
                            tubes and was massive in size. The invention of the **transistor (1947)** revolutionized computing, making machines smaller, faster, and more reliable.  
                            The latter half of the 20th century introduced **integrated circuits, microprocessors, and personal computers**, leading to the digital revolution. Today, computers are 
                            integral to nearly every aspect of life, from smartphones to artificial intelligence, continuing to evolve at an unprecedented pace.""" 

    save_conversation(test_user, long_user_input, long_assistant_reply)
