import datetime

from database import *
from reset_password import *
def archive_and_delete_customer():
    username = input('enter your username :')
    temp = db_query(f"SELECT email from CUSTOMERS where username = '{username}';")
    if temp:
        email = temp[0][0]
        otp = generate_otp()
        print(f"Generated OTP: {otp}")
        send_otp(email,otp)
        print(f"An OTP has been sent to {email}")
        user_otp = input('Enter the OTP :')
        # Debugging: Print both OTPs to verify they match
        print(f"User OTP (entered): '{user_otp}', Generated OTP: '{otp}'")
        if user_otp == otp:
            customer_data = db_query(f"SELECT * from customers where username = '{username}';")
            if customer_data:
                customer_data = customer_data[0]
                deleted_at = datetime.date.today()
                username, salt , hashed_password, name, age, city, balance, account_number, email,inserted_at, status = customer_data
                archive_query = f"""
                        INSERT INTO customers_archive 
                        (username, password, name, age, city, balance, account_number, email, deleted_at, status)
                        VALUES ('{username}', '{salt}','{hashed_password}', '{name}', {age}, '{city}', {balance}, {account_number}, '{email}', '{deleted_at}', {status});
                        """
                cursor.execute(archive_query)
                mydb.commit()

                delete_query = f"DELETE from customers where username = '{username}';"
                cursor.execute(delete_query)
                mydb.commit()
                print(f"Customer with username '{username}' has been archived and deleted from active customers")
            else:
                print(f"No customer found with username '{username}'")
        else:
            print('Invalid input')
            return exit()