from customer import *
from bank import Bank
import random
def SignUp():
    username = input("create username :")
    temp = db_query(f"SELECT username from customers where username = '{username}';")
    if temp:
        print('username Already Exists')
        SignUp()
    else :
        print('Username is Available please proceed')
        password = input('enter your password')
        name = input("Enter Your Name: ")
        age = input("Enter Your Age: ")
        city = input('Enter your city :')
        while True :
            account_number = int(random.randint(10000000, 99999999))
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if temp :
                continue
            else:
                print(account_number)
                break
        cobj = Customer(username, password, name, age, city, account_number)
        cobj.createuser()
        bobj = Bank(username, account_number)
        bobj.create_transaction_table()

def SignIn():
    username = input('Enter username:')
    temp = db_query(f"SELECT username from customers where username = '{username}';")
    if temp :
        while True:
            password = input(f"Welcome {username.capitalize()} Enter password")
            temp = db_query(f"SELECT password from customers where password = '{password}';")
            # print(temp[0][0])
            if temp and temp[0][0]== password :
                print("Sign IN Succesfully")
                return username
            else:
                print("Wrong Password Try Again")
                continue

    else:
        print("Enter Correct Username")
        SignIn()