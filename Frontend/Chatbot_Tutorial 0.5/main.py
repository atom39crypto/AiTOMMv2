import eel

eel.init("web")  # The "web" folder should contain your index.html, script.js, and style.css

@eel.expose
def get_response(user_message):
    responses = {
        "hello": "Hi there! 😊",
        "how are you": "I'm great! How about you? 🤖",
        "bye": "Goodbye! Have a wonderful day! 👋",
        "who are you": "I'm Atom, your chatbot assistant! 🚀",
    }
    response = responses.get(user_message.lower(), "Sorry, I don't understand that. 🤔")
    print(f"User: {user_message} -> Bot: {response}")  # Debug log
    return response

if __name__ == "__main__":
    print("Starting chatbot...")
    eel.start("index.html", size=(600, 600))
