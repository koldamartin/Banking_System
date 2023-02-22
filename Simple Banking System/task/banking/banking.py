import random

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
    card_number = input("\nEnter your card number:\n>")
    card_pin = input("Enter your PIN:\n>")
    if card_number in card_database and card_database[card_number] == card_pin:
        print("\nYou have successfully logged in!\n")
        check_balance()
    else:
        print("\nWrong card number or PIN!\n")

def check_balance():
    logged = True
    while logged:
        choice_while_logged = input("1. Balance\n2. Log out\n0. Exit\n>")
        if choice_while_logged == "1":
            print("\nBalance: 0\n")
        elif choice_while_logged == "2":
            print("\nYou have successfully logged out!\n")
            logged = False
        elif choice_while_logged == "0":
            logged = False

def create_new_account():
    new_card_number = generate_card_no()
    new_card_pin = generate_pin()
    card_database[new_card_number] = new_card_pin
    print(f"\nYour card has been created\nYour card number:\n{new_card_number}\nYour card PIN:\n{new_card_pin}\n")

card_database = {}
banking_on = True
while banking_on:
    your_choice = (input("1. Create an account\n2. Log into account\n0. Exit\n>"))

    if your_choice == "1":
        create_new_account()

    elif your_choice == "2":
        check_log_in()

    elif your_choice == "0":
        print("\nBye!")
        banking_on = False
