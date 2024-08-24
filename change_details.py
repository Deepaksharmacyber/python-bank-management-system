from reset_password import *

def change_details(out):
    username = input('enter your username :')
    temp = db_query(f"SELECT email from CUSTOMERS where username = '{username}';")
    if temp :
        email = temp[0][0]
        otp = generate_otp()
        send_otp(email,otp)
        print(f"An OTP has been sent to {email}")
        user_otp = int(input('Enter the OTP :'))
        if user_otp == otp:
            new_detail = input(f"Enter your new {out}")
            db_query(f"UPDATE customers SET {out} = '{new_detail}' where username = '{username}';")
            mydb.commit()
            print(f"{out} has been updated succesfully")
        else :
            print(f'Invalid password ,Please try again')
    else :
        print(f'username is not found , Please try again')