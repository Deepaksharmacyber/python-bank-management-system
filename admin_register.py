# from datetime import date
# from customer import *
# from bank import *
# from savings_fixed_deposits import *
# from password_maker import *
# import random
from reset_password import *
from database import *
import hashlib



def AdminSignUp():
    username = input("Create admin username: ")
    temp = db_query(f"SELECT username FROM admins WHERE username = '{username}';")
    if temp:
        print('Username already exists')
        AdminSignUp()
    else:
        print('Username is available, please proceed')
        password = get_valid_password()
        salt, hashed_password = hash_password(password)
        name = input("Enter your name: ")
        gender = input("Enter your gender: ")
        age = int(input("Enter your age: "))
        city = input("Enter your city: ")
        nationality = input("Enter your nationality: ")
        position_name = input("Enter your position in the bank: ")
        salary = float(input("Enter your salary: "))
        working_status = True

        cursor.execute('''
            INSERT INTO admins (username, salt, password, name, gender, age, city, nationality, position_name,working_status, salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)
        ''', (username, salt, hashed_password, name, gender, age, city, nationality, position_name,working_status, salary))
        mydb.commit()
        print("Admin registered successfully!")

def AdminSignIn():
    username = input('Enter admin username: ')
    temp = db_query(f"SELECT username FROM admins WHERE username = '{username}';")
    if temp:
        count_of_enter_passwords = 0
        while True:
            count_of_enter_passwords += 1
            password = input(f"Welcome {username.capitalize()}, enter password: ")
            user_data = db_query(f"SELECT password, salt FROM admins WHERE username = '{username}';")
            stored_password, stored_salt = user_data[0]
            hashed_input_password = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt, 100000)

            if hashed_input_password == stored_password:
                print("Sign IN Successfully")
                return username
            elif count_of_enter_passwords == 3:
                print('Too many wrong attempts. Try again later.')
                return None
            else:
                print("Wrong Password")
    else:
        print("Enter correct username")
        return None


# AdminSignUp()