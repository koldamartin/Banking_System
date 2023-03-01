import random
import sqlite3

conn = sqlite3.connect('card.s3db')  # create a connection object that represents the database
cur = conn.cursor()  # create a cursor object

def generate_card_no():
    first_digits = str(400000)
    second_digits = str(random.randint(100000000,999999999))
    all_digits = first_digits + second_digits + luhn_algorithm(first_digits, second_digits)
    return all_digits

def luhn_algorithm(first, second):
    """the input is all the digits from the card except the last one. The output is the last number"""
    check_sum = ""
    all_digits = first + second
    for i in range(len(all_digits)):
        if i % 2 == 0:
            multiplied = str(int(all_digits[i]) * 2)
            if int(multiplied) > 9:
                substracted = str(int(multiplied) - 9)
                check_sum += substracted
            else:
                check_sum += multiplied
        else:
            check_sum += all_digits[i]
    sum = 0
    for number in check_sum:
        sum += int(number)

    for i in range(0, 10):
        if (i+sum) % 10 == 0:
            last_digit = i
    return str(last_digit)

def generate_pin():
    create_pin = [str(random.randint(0, 9)) for x in range(4)]
    return ''.join(i for i in create_pin)

def check_log_in():
    global card_number
    card_number = input("\nEnter your card number:\n>")
    card_pin = input("Enter your PIN:\n>")
    account_exists_check = cur.execute("SELECT id FROM card WHERE number = ?", (card_number,)).fetchone()
    result = cur.execute(f"SELECT pin FROM card WHERE number IN ({card_number})").fetchone()
    if account_exists_check is not None and result[0] == card_pin:
        print("\nYou have successfully logged in!\n")
        return True
    else:
        print("\nWrong card number or PIN!\n")

def create_new_account():
    cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT,pin TEXT,balance INTEGER DEFAULT 0)")
    conn.commit()
    new_card_number = generate_card_no()
    new_card_pin = generate_pin()
    cur.execute(f"INSERT INTO card (number, pin) VALUES ({new_card_number}, {new_card_pin})")
    conn.commit()
    print(f"\nYour card has been created\nYour card number:\n{new_card_number}\nYour card PIN:\n{new_card_pin}\n")

def find_balance():
    balance = cur.execute(f"SELECT balance FROM card WHERE number IN ({card_number})").fetchone()
    print(f"\nBalance: {balance[0]}\n")

def add_income():
    income = int(input("\nEnter income:\n>"))
    sending_acc_balance = cur.execute("SELECT balance FROM card WHERE number = ?", (card_number,)).fetchone() #hruza upravit
    cur.execute("UPDATE card SET balance = ? WHERE number = ?", (sending_acc_balance[0] + income, card_number))
    conn.commit()
    print("Income was added\n")

def transfer():
    target_account = input("\nTransfer\nEnter card number:\n>")
    target_acc_balance = cur.execute("SELECT balance FROM card WHERE number = ?", (target_account,)).fetchone()
    if target_account[-1] != luhn_algorithm(target_account[:6], target_account[6:-1]): #check if acc_num passes the luhn's algorithm
        print("Probably you made a mistake in the card number. Please try again!\n")
    elif target_acc_balance is None: #check if the card number exists
        print("Such a card does not exist.\n")
    elif target_account == card_number: #check if you are not sending money to the same account
        print("You can't transfer money to the same account!\n")
    else:
        transfered_amount = int(input("Enter how much money you want to transfer:\n>"))
        sending_acc_balance = cur.execute("SELECT balance FROM card WHERE number = ?", (card_number,)).fetchone()
        if transfered_amount <= sending_acc_balance[0]: #check if you have enough money
            cur.execute("UPDATE card SET balance = ? WHERE number = ?", (sending_acc_balance[0] - transfered_amount, card_number)) #sending acc.
            cur.execute("UPDATE card SET balance = ? WHERE number = ?", (target_acc_balance[0] + transfered_amount, target_account)) #target acc.
            conn.commit()
            print("\nSucces!\n")
        else:
            print("\nNot enough money!\n")

def delete_account():
    cur.execute("DELETE FROM card WHERE number = ?", (card_number,))
    conn.commit()
    print("\nThe account has been closed!\n")

banking_on = True
while banking_on:
    your_choice = (input("1. Create an account\n2. Log into account\n0. Exit\n>"))

    if your_choice == "1":
        create_new_account()
        #print(cur.execute("SELECT * FROM card").fetchall()) #pak smazat

    elif your_choice == "2":
        if check_log_in() == True:
            logged = True
            while logged:
                choice_while_logged = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n>")
                if choice_while_logged == "1": #Balance
                    find_balance()
                elif choice_while_logged == "2": #Add income
                    add_income()
                elif choice_while_logged == "3": #Do transfer
                    transfer()
                elif choice_while_logged == "4": #Close account
                    delete_account()
                    logged = False
                elif choice_while_logged == "5": #Log out
                    print("\nYou have successfully logged out!\n")
                    logged = False
                elif choice_while_logged == "0": #Exit
                    print("\nBye!\n")
                    logged = False
                    banking_on = False

    elif your_choice == "0":
        print("\nBye!")
        banking_on = False
