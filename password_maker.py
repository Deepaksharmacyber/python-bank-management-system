import re
import hashlib
import os
import secrets
import string


def get_valid_password():
    while True:
        choice = input(
            "Would you like to (1) enter a password manually or (2) auto-generate a password? Enter 1 or 2: ")

        if choice == '1':
            while True:
                print("Password must be at least 8 characters long.")
                print("Password must contain at least one lowercase letter.")
                print("Password must contain at least one uppercase letter.")
                print("Password must contain at least one number.")
                print("Password must contain at least one special character.")
                password = input("Enter your password: ")

                if len(password) < 8:
                    print("Password must be at least 8 characters long.")
                    continue

                if not re.search("[a-z]", password):
                    print("Password must contain at least one lowercase letter.")
                    continue

                if not re.search("[A-Z]", password):
                    print("Password must contain at least one uppercase letter.")
                    continue

                if not re.search("[0-9]", password):
                    print("Password must contain at least one number.")
                    continue

                if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
                    print("Password must contain at least one special character.")
                    continue

                print("Password is valid.")
                return password

        elif choice == '2':
            password = auto_generate_password()
            print(f"Auto-generated password: {password}")
            return password

        else:
            print("Invalid choice. Please enter 1 or 2.")


def auto_generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))

    # Ensure the generated password meets all criteria
    while (not re.search("[a-z]", password) or
           not re.search("[A-Z]", password) or
           not re.search("[0-9]", password) or
           not re.search("[!@#$%^&*(),.?\":{}|<>]", password)):
        password = ''.join(secrets.choice(characters) for _ in range(length))

    return password


def hash_password(password):
    salt = os.urandom(16)
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt, hashed_password


def verify_password(stored_password, stored_salt, password):
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), stored_salt, 100000)
    return hashed_password == stored_password


# # Example usage
# password = get_valid_password()
# salt, hashed_password = hash_password(password)
# print("Password hashed and salted.")
