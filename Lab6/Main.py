import sqlite3
from faker import Faker
import random

fake = Faker('uk_UA')

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    registration_date TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category_id INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (account_id) REFERENCES Accounts(id),
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);
''')

users = []
for _ in range(5):
    name = fake.name()
    email = fake.email()
    registration_date = fake.date_this_decade().isoformat()
    cursor.execute("INSERT INTO Users (name, email, registration_date) VALUES (?, ?, ?)",
                   (name, email, registration_date))
    users.append(cursor.lastrowid)

categories = ["Їжа", "Транспорт", "Розваги", "Комунальні послуги", "Покупки"]
category_ids = {}
for category in categories:
    cursor.execute("INSERT INTO Categories (name) VALUES (?)", (category,))
    category_ids[category] = cursor.lastrowid

for user_id in users:
    balance = round(random.uniform(100, 5000), 2)
    cursor.execute("INSERT INTO Accounts (user_id, balance) VALUES (?, ?)", (user_id, balance))
    account_id = cursor.lastrowid

    for _ in range(5):
        amount = round(random.uniform(5, 500), 2)
        category_id = random.choice(list(category_ids.values()))
        transaction_date = fake.date_time_this_year().isoformat()
        cursor.execute(
            "INSERT INTO Transactions (user_id, account_id, amount, category_id, transaction_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, account_id, amount, category_id, transaction_date))

cursor.execute('''
SELECT Users.name, Users.email, Transactions.amount, Categories.name, Transactions.transaction_date
FROM Users
JOIN Transactions ON Users.id = Transactions.user_id
JOIN Categories ON Transactions.category_id = Categories.id;
''')
print("Користувачі та їхні транзакції:")
print(cursor.fetchall())

cursor.execute("SELECT email FROM Users WHERE id = ?", (users[0],))
email = cursor.fetchone()[0]
cursor.execute('''
SELECT SUM(Transactions.amount)
FROM Transactions
JOIN Users ON Transactions.user_id = Users.id
WHERE Users.email = ?;
''', (email,))
print("Загальна сума транзакцій користувача:")
print(cursor.fetchone())

category_name = "Їжа"
cursor.execute('''
SELECT MAX(Transactions.amount)
FROM Transactions
JOIN Categories ON Transactions.category_id = Categories.id
WHERE Categories.name = ?;
''', (category_name,))
print("Найбільша транзакція в категорії:")
print(cursor.fetchone())

cursor.execute('''
SELECT Users.name, Users.email, Accounts.id AS account_id, Accounts.balance
FROM Users
JOIN Accounts ON Users.id = Accounts.user_id;
''')

print("Акаунти користувачів та їхні баланси:")
for row in cursor.fetchall():
    print(row)

cursor.execute('''
SELECT Categories.name AS category, MAX(Transactions.amount) AS max_transaction
FROM Transactions
JOIN Categories ON Transactions.category_id = Categories.id
GROUP BY Categories.name;
''')

print("Найбільші транзакції в кожній категорії:")
for row in cursor.fetchall():
    print(row)

conn.commit()
conn.close()
