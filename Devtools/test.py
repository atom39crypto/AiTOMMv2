# Training data
messages = [
    ("win money now", "spam"),
    ("cheap meds available", "spam"),
    ("meet me for lunch", "ham"),
    ("how are you", "ham")
]

# Step 1: Build vocabulary and count word frequencies
word_counts = {"spam": {}, "ham": {}}
class_counts = {"spam": 0, "ham": 0}
vocab = set()

for text, label in messages:
    class_counts[label] += 1
    words = text.split()
    for word in words:
        vocab.add(word)
        if word in word_counts[label]:
            word_counts[label][word] += 1
        else:
            word_counts[label][word] = 1

# Step 2: Calculate prior probabilities
total_messages = len(messages)
prior_spam = class_counts["spam"] / total_messages
prior_ham = class_counts["ham"] / total_messages

# Step 3: Define prediction function
def predict(text):
    words = text.split()
    # Start with log of prior probabilities
    spam_score = prior_spam
    ham_score = prior_ham

    for word in words:
        # Use Laplace smoothing (add-one smoothing)
        spam_word_prob = (word_counts["spam"].get(word, 0) + 1) / (sum(word_counts["spam"].values()) + len(vocab))
        ham_word_prob = (word_counts["ham"].get(word, 0) + 1) / (sum(word_counts["ham"].values()) + len(vocab))

        spam_score *= spam_word_prob
        ham_score *= ham_word_prob

    return "spam" if spam_score > ham_score else "ham"

# Step 4: Try some predictions
test_messages = [
    "win cheap offer",
    "are you free for lunch",
    "money available now",
    "how are you"
]

for msg in test_messages:
    print(f"'{msg}' => {predict(msg)}")
