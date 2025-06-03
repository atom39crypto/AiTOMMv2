import re
import sqlite3
from groq import Groq

FILE_PATH = r"Core/Memo/memory.db"

def summarizer(user_data):
    client = Groq(api_key="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")
    try:
        if isinstance(user_data, str):
            user_data = user_data.strip()

        prompt = f"Create a report from the following user data: {user_data}"

        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        """From the conversations provided, create a report of the person in the structure:
                        {
                            \"Name\": "",
                            \"overall_personality\": "",
                            \"interests\": "",
                            \"Other important informations\": "",
                            \"important informations for assistant\": "",
                            \"first_update\": "{datetime.now().isoformat()}"
                            \"last_updated\": "{datetime.now().isoformat()}"
                        }
                        Do not provide anything else before or after."""
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1,
            max_tokens=130000,
            top_p=1,
            stream=False
        )

        report = completion.choices[0].message.content
        return report

    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_table_data(target_tables):
    conn = sqlite3.connect(FILE_PATH)
    cursor = conn.cursor()

    data = ""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = {table[0] for table in cursor.fetchall()}  # Set for faster lookup

    # Filter the target tables that actually exist in the database
    valid_tables = [table for table in target_tables if table in all_tables]
    invalid_tables = [table for table in target_tables if table not in all_tables]

    if invalid_tables:
        print(f"Warning: These tables do not exist in the database: {', '.join(invalid_tables)}")

    all_tables_data = {}

    for table_name in valid_tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()
        col_names = [col[1] for col in columns_info]

        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        # If the table has a 'content' column, truncate its value to the first 20 words
        if 'content' in col_names and 'role' in col_names:
            content_index = col_names.index('content')
            role_index = col_names.index('role')
            modified_rows = []
            for row in rows:
                if row[role_index] == 'user':  # Only process rows where the role is 'User'
                    row_list = list(row)
                    if row_list[content_index]:
                        words = row_list[content_index].split()
                        row_list[content_index] = " ".join(words[:20])
                        modified_rows.append(tuple(row_list))
            rows = modified_rows
            # print(rows)
            data += summarizer(rows) + "\n"

        all_tables_data[table_name] = rows

    conn.close()
    data = re.sub(r'.*?({.*?}).*', r'\1', data, flags=re.DOTALL)
    with open("Core/Memo/person_report.txt", "w") as file:
        file.write(data)


if __name__ == "__main__":
    # Example: User specifies the tables to retrieve data from
    user = ['Shounak']  # Replace with actual table names
    data = get_table_data(user)
    print(data)
