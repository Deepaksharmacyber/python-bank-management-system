# from datetime import date , datetime
from customer import *
from bank import *
from savings_fixed_deposits import *
# from password_maker import *
# import random
from reset_password import *
MINIMUM_BALANCE_SAVINGS = 1000
def SignUp():
    username = input("create username :")
    temp = db_query(f"SELECT username from customers where username = '{username}';")
    if temp:
        print('username Already Exists')
        SignUp()
    else :
        print('Username is Available please proceed')
        password = get_valid_password()
        salt, hashed_password = hash_password(password)
        name = input("Enter Your Name: ")
        age = input("Enter Your Age: ")
        city = input('Enter your city :')
        email = input('enter your email :')
        creation_date = date.today()
        print(f'creation date is {creation_date}')

        while True:
            account_type = input("Select account type (Savings/Current): ").strip().lower()
            if account_type in ['savings', 'current']:
                break
            else:
                print("Invalid account type. Please choose 'Savings' or 'Current'.")

        if account_type == 'savings':
            while True:
                try:
                    initial_deposit = int(input(
                        f"Enter initial deposit amount (Minimum {MINIMUM_BALANCE_SAVINGS} for savings account): "))
                    if initial_deposit >= MINIMUM_BALANCE_SAVINGS:
                        break
                    else:
                        print(f"Initial deposit must be at least {MINIMUM_BALANCE_SAVINGS}.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        else:
            initial_deposit = 0

        while True :
            account_number = int(random.randint(10000000, 99999999))
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if temp :
                continue
            else:
                print(account_number)
                break
        cobj = Customer(username, salt, hashed_password, name, age, city, account_number,email,creation_date,account_type,initial_deposit)
        cobj.createuser()
        bobj = Bank(username, account_number)
        bobj.create_transaction_table()

def SignIn():
    username = input('Enter username:')
    temp = db_query(f"SELECT username from customers where username = '{username}';")
    if temp :
        count_of_enter_passwords = 0
        while True:
            count_of_enter_passwords += 1
            password = input(f"Welcome {username.capitalize()} Enter password")
            # stored_password, stored_salt = db_query(f"SELECT password,salt from customers where password = '{password}';")
            # print(temp[0][0])

            user_data = db_query(f"SELECT password, salt FROM customers WHERE username = '{username}';")
            stored_password, stored_salt = user_data[0]
            hashed_input_password = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt, 100000)


            if hashed_input_password == stored_password:
                print("Sign IN Successfully")
                # Create the Bank object here
                account_number = db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")[0][0]
                account_type = db_query(f"SELECT account_type FROM customers WHERE account_number = '{account_number}';")[0][0]
                if account_type == 'savings':
                    bobj = SavingsFixedDeposits(account_number)
                    bobj.check_and_add_fixed_deposit_interest()
                return username

            elif count_of_enter_passwords == 3:
                print('Your password is reseting , fill the given details')
                reset_password()
                return username
            else:
                print("Wrong Password")
                print('Do you want to create a new password --> YES or NO')
                out = input('').lower()
                if out == 'yes':
                    ans = reset_password()
                    if ans == 'no':
                        return exit()
                    else :
                        return username
                else :
                    continue

    else:
        print("Enter Correct Username")
        return exit()