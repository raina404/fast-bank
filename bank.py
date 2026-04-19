import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

#https://docs.python.org/3/library/sqlite3.html
#https://www.sqlitetutorial.net/sqlite-create-table/


#make table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance REAL DEFAULT 0.00
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        amount REAL NOT NULL,
        transaction_type TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
""")

conn.commit()

#menu display
def display_menu():
    print("\n-----BANKING APP MENU-----")
    print("1. Create a new bank account")
    print("2. Deposit money")
    print("3. Withdraw money")
    print("4. Check account balance")
    print("5. List all accounts")
    print("6. Exit")

#create account
def create_account():
    name = input("Account name: ")
    initial = float(input("Initial deposit: $"))
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, initial))
    conn.commit()
    cursor.execute("INSERT INTO transactions (account_id, amount, transaction_type) VALUES (?, ?, 'deposit')", (cursor.lastrowid, initial))
    conn.commit()
    print(f"Account created for {name} with ${initial}!")

#deposoit
def deposit_to_account():
    name = input("Account name: ")
    cursor.execute("SELECT id, balance FROM accounts WHERE name = ?", (name,))
    account = cursor.fetchone()
    if account is None:
        print("Account not found.")
    else:
        amount = float(input("Amount to deposit: $"))
        cursor.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, name))
        cursor.execute("INSERT INTO transactions (account_id, amount, transaction_type) VALUES (?, ?, 'deposit')", (account[0], amount))
        conn.commit()
        print(f"Deposited ${amount}!")

#withdraw
def withdraw_from_account():
    name = input("Account name: ")
    cursor.execute("SELECT id, balance FROM accounts WHERE name = ?", (name,))
    account = cursor.fetchone()
    if account is None:
        print("Account not found.")
    else:
        amount = float(input("Amount to withdraw: $"))
        if account[1] < amount:
            print("Not enough money!")
        else:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?", (amount, name))
            cursor.execute("INSERT INTO transactions (account_id, amount, transaction_type) VALUES (?, ?, 'withdrawal')", (account[0], amount))
            conn.commit()
            print(f"Withdrew ${amount}!")

#check balance
def check_balance():
    name = input("Account name: ")
    cursor.execute("SELECT balance FROM accounts WHERE name = ?", (name,))
    account = cursor.fetchone()
    if account is None:
        print("Account not found.")
    else:
        print(f"Balance: ${account[0]}")

#list accounts
def list_accounts():
    cursor.execute("SELECT id, name, balance FROM accounts")
    accounts = cursor.fetchall()
    if len(accounts) == 0:
        print("No accounts found.")
    else:
        print("\n--- All Accounts ---")
        for account in accounts:
            print(f"ID: {account[0]} | Name: {account[1]} | Balance: ${account[2]}")

#choice loop
while True:
    display_menu()
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        create_account()
    elif choice == "2":
        deposit_to_account()
    elif choice == "3":
        withdraw_from_account()
    elif choice == "4":
        check_balance()
    elif choice == "5":
        list_accounts()
    elif choice == "6":
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid option. Try again with a number from 1-6.")