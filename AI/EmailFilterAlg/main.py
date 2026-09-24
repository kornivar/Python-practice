import os

os.makedirs("SPAM", exist_ok=True)
os.makedirs("NOTSPAM", exist_ok=True)

SPAMWORDS: list[str] = []
MARKEDUSERS: list[str] = []

with open("data/SPAMWORDS.txt", "r", encoding="utf-8") as file:
    SPAMWORDS = [word.strip() for word in file]

with open("data/MARKEDUSERS.txt", "r", encoding="utf-8") as file:
    MARKEDUSERS = [word.strip() for word in file]

with open("data/emails.txt", "r", encoding="utf-8") as f:
    blocks = f.read().split("\n\n")

messages: list[dict] = []

for block in blocks:
    message = {}

    for line in block.splitlines():
        key, value = line.split(": ", 1)
        message[key] = value

    messages.append(message)


def create_spam_txt(filename, message):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"from: {message['from']}\n")
        file.write(f"text: {message['text']}\n")
        file.write(f"date: {message['date']}\n")

def add_spam_email(email):
    with open("data/MARKEDUSERS.txt", "a", encoding="utf-8") as file:
        file.write(f"{email}\n")


for message in messages:
    username = message["from"].split("@")[0]

    if message["from"] in MARKEDUSERS:
        create_spam_txt(f"SPAM/{username}_SPAM.txt", message)
        continue

    if any(word in message["text"].lower() for word in SPAMWORDS):
        add_spam_email(message["from"])
        create_spam_txt(f"SPAM/{username}_SPAM.txt", message)
    else:
        create_spam_txt(f"NOTSPAM/{username}.txt", message)
