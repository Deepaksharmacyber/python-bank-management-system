from database import *
import datetime

class Customer:
    def __init__(self,username,salt , hashed_password, name, age, city, account_number,email,creation_date,account_type,initial_deposit):
        self.__username = username
        self.__salt = salt
        self.__hashed_password = hashed_password
        self.__name = name
        self.__age = age
        self.__city = city
        self.__account_number = account_number
        self.__email = email
        self.__created_at = creation_date
        self.__account_type = account_type
        self.__last_interest_date = creation_date
        self.__initial_deposit = initial_deposit


    def createuser(self):
        query = '''
            INSERT INTO customers 
            (username, salt, password, name, age, city, balance, account_number, email, created_at, status,account_type
            ,last_interest_date,withdrawals_this_month, transfers_this_month, last_reset_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
        '''
        values = (
            self.__username, self.__salt, self.__hashed_password, self.__name, self.__age,
            self.__city,self.__initial_deposit, self.__account_number, self.__email, self.__created_at, 1,self.__account_type,
            self.__last_interest_date , 0 , 0 , datetime.date.today()
        )
        cursor.execute(query, values)
        mydb.commit()