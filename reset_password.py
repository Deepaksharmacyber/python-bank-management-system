import smtplib
import random
from password_maker import *
from database import *


def generate_otp():
    return random.randint(100000, 999999)

def send_otp(email, otp):
    # Set up the SMTP server (you may need to configure this with your email provider's settings)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email_id', 'password') #this will be not your regular password of gmail, this password will generate when you will on smtp services on your gmail
    message = f"Your OTP is {otp}"
    server.sendmail('sender gmail-id', email, message)
    server.quit()

def reset_password():
    username = input('enter your username :')
    temp = db_query(f"SELECT email from CUSTOMERS where username = '{username}';")
    if temp :
        email = temp[0][0]
        otp = generate_otp()
        send_otp(email,otp)
        print(f"An OTP has been sent to {email}")
        user_otp = int(input('Enter the OTP :'))
        if user_otp == otp:
            # new_password = input("enter your new password")
            password = get_valid_password()
            salt, hashed_password = hash_password(password)
            query = f"UPDATE customers SET password = %s, salt = %s WHERE username = %s;"
            values = (hashed_password, salt, username)
            cursor.execute(query, values)
            mydb.commit()
            print(f'password has been succesfully updated')
            return exit()
        else:
            print(f'Invalid OTP ,Please try again')
            return 'no'
    else :
        print(f'username is not found , Please try again')
        return 'no'