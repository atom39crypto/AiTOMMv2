import json
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

def load_memory_from_json(filepath: str):
    """
    Load conversation messages from a JSON file and convert them to LangChain message objects.
    The JSON file should contain a list of dictionaries with 'role' and 'content' keys.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        messages_data = json.load(file)

    converted_messages = []
    for msg in messages_data:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            converted_messages.append(HumanMessage(content=content))
        elif role == "assistant":
            converted_messages.append(AIMessage(content=content))
        else:
            raise ValueError(f"Unexpected role encountered: {role}")
    return converted_messages

def messages_to_dict(messages):
    """
    Convert a list of LangChain message objects back into a list of dictionaries.
    """
    result = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            role = "unknown"
        result.append({"role": role, "content": msg.content})
    return result

# Load messages from the JSON file.
loaded_messages = load_memory_from_json("memory.json")

# Create a ConversationBufferMemory instance.
memory = ConversationBufferMemory(return_messages=True)

# Populate the conversation memory with the loaded messages.
for message in loaded_messages:
    memory.chat_memory.messages.append(message)

# Optionally, convert the conversation memory back to a list of dictionaries.
memory_as_dict = messages_to_dict(memory.chat_memory.messages)

# Print the memory in dictionary format.
print(memory_as_dict)
