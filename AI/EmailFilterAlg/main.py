import os

os.makedirs("SPAM", exist_ok=True)
os.makedirs("NOTSPAM", exist_ok=True)

with open("emails.txt", "r", encoding="utf-8") as f:
    blocks = f.read().split("\n\n")

messages: list[dict] = []
SPAMWORDS: list[str] = [
    "free",
    "winner",
    "congratulations",
    "prize",
    "bonus",
    "discount",
    "offer",
    "promotion",
    "sale",
    "limited time",
    "buy now",
    "click here",
    "act now",
    "claim",
    "claim your prize",
    "you won",
    "urgent",
    "exclusive",
    "cash",
    "money",
    "earn money",
    "make money",
    "investment",
    "crypto",
    "bitcoin",
    "loan",
    "credit",
    "casino",
    "jackpot",
    "lottery",
    "viagra",
    "unsubscribe",

    "безкоштовно",
    "виграли",
    "перемога",
    "приз",
    "подарунок",
    "бонус",
    "знижка",
    "акція",
    "пропозиція",
    "терміново",
    "заробіток",
    "заробити",
    "гроші",
    "інвестиція",
    "криптовалюта",
    "кредит",
    "казино",
    "лотерея",
    "натисніть",
    "перейдіть за посиланням",

    "бесплатно",
    "вы выиграли",
    "победитель",
    "приз",
    "подарок",
    "бонус",
    "скидка",
    "акция",
    "предложение",
    "срочно",
    "заработок",
    "заработать",
    "деньги",
    "инвестиции",
    "криптовалюта",
    "кредит",
    "казино",
    "лотерея",
    "депозит",
    "инвестируйте",
    "нажмите",
    "перейдите по ссылке",
]
MARKEDUSERS: list[str] | list[None] = []


for block in blocks:
    message = {}

    for line in block.splitlines():
        key, value = line.split(": ", 1)
        message[key] = value

    messages.append(message)


def create_txt(filename, message):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"from: {message['from']}\n")
        file.write(f"text: {message['text']}\n")
        file.write(f"date: {message['date']}\n")


for message in messages:
    username = message["from"].split("@")[0]

    if message["from"] in MARKEDUSERS:
        create_txt(f"SPAM/{username}_SPAM.txt", message)
        continue

    if any(word in message["text"].lower() for word in SPAMWORDS):
        MARKEDUSERS.append(message["from"])
        create_txt(f"SPAM/{username}_SPAM.txt", message)
    else:
        create_txt(f"NOTSPAM/{username}.txt", message)

print(MARKEDUSERS)