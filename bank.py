from database import *
from datetime import datetime, date , timedelta

class Bank:

    def __init__(self,username,account_number):
        self.__username = username
        self.__account_number = account_number
        self.__transaction_counts = self.get_transaction_counts()


    MAX_WITHDRAWALS = 5  # maximum number of withdrawals allowed per month
    MAX_TRANSFERS = 5  # maximum number of fund transfers allowed per month

    MINIMUM_BALANCE_SAVINGS = 1000

# ----------------------------------------------transactions counts---------------------------------------------
    def get_transaction_counts(self):
        result = db_query(
            f"SELECT withdrawals_this_month, transfers_this_month, last_reset_date FROM customers WHERE account_number = '{self.__account_number}';")
        if result:
            return {'withdrawals': result[0][0], 'transfers': result[0][1], 'last_reset': result[0][2]}
        else:
            return {'withdrawals': 0, 'transfers': 0, 'last_reset': date.today()}

    def reset_transaction_limits(self):
        today = date.today()
        if self.__transaction_counts['last_reset'].month != today.month or self.__transaction_counts[
            'last_reset'].year != today.year:
            self.__transaction_counts = {'withdrawals': 0, 'transfers': 0, 'last_reset': today}
            db_query(
                f"UPDATE customers SET withdrawals_this_month = 0, transfers_this_month = 0, last_reset_date = '{today}' WHERE account_number = '{self.__account_number}';")
            mydb.commit()



    def create_transaction_table(self):
        db_query(f"CREATE TABLE IF NOT EXISTS {self.__username}_transaction "
                 f"( timedate VARCHAR(30),"
                 f"account_number INTEGER,"
                 f"remarks VARCHAR(30),"
                 f"amount INTEGER )")

    def view_transactions(self):
        transactions = db_query(f"SELECT * from {self.__username}_transaction ;")
        if transactions:
            print(f"Transactions for {self.__username} :")
            for transaction in transactions:
                print(transaction)
        else :
            print(f"No transactions found for {self.__username} :")

    def balanceequiry(self):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        print(f"{self.__username} Balance is {temp[0][0]}")

    def deposit(self, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        test = temp[0][0] + amount

        db_query(
            f"UPDATE customers SET balance = '{test}' WHERE username = '{self.__username}'; ")

        self.balanceequiry()
        db_query(f"INSERT INTO {self.__username}_transaction Values ("
                 f"'{datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Depoist',"
                 f"'{amount}'"
                 f")")

        print(f"{self.__username} Amount is Sucessfully Depositted into Your Account {self.__account_number}")

    def withdraw(self):
        account_type = self.get_account_type()
        if account_type == 'savings':
            self.reset_transaction_limits()
            if self.__transaction_counts['withdrawals'] >= self.MAX_WITHDRAWALS:
                print("Monthly withdrawal limit reached.")
                return False

        amount = int(input("Enter Amount to Withdraw"))
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")

        if amount > temp[0][0]:
            print("Insufficient Balance Please Deposit Money")
        elif (temp[0][0] - amount) < self.MINIMUM_BALANCE_SAVINGS:
            print(f"Cannot withdraw. Minimum balance of {self.MINIMUM_BALANCE_SAVINGS} must be maintained.")
        else:
            new_balance = temp[0][0] - amount
            db_query(
                f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
            self.balanceequiry()
            db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                     f"'{datetime.now()}',"
                     f"'{self.__account_number}',"
                     f"'Amount Withdraw',"
                     f"'{amount}'"
                     f")")
            # account_type = self.get_account_type()
            # if account_type == 'savings':
            self.__transaction_counts['withdrawals'] += 1
            db_query(
                    f"UPDATE customers SET withdrawals_this_month = {self.__transaction_counts['withdrawals']} WHERE account_number = '{self.__account_number}';")

            print(f"{self.__username} Amount is Sucessfully Withdraw from Your Account {self.__account_number}")

#----------------------------------------------fundtransfer code---------------------------------------------
    def fundtransfer(self, receive, amount):
        receiver_account = db_query(f"SELECT balance FROM customers WHERE account_number = '{receive}';")
        if not receiver_account:
            print(f'This account number {receive} does not exist.')
            return

        account_type = self.get_account_type()
        if account_type == 'savings':
            self.reset_transaction_limits()
            if self.__transaction_counts['transfers'] >= self.MAX_TRANSFERS:
                print("Monthly fund transfer limit reached.")
                return False

        sender_balance = db_query(f"SELECT balance FROM customers WHERE username = '{self.__username}';")

        if amount > sender_balance[0][0]:
            print('Insufficient Balance. Please Deposit Money.')
            return

        if account_type == 'savings' and (sender_balance[0][0] - amount) < self.MINIMUM_BALANCE_SAVINGS:
            print(f"Cannot withdraw. Minimum balance of {self.MINIMUM_BALANCE_SAVINGS} must be maintained.")
            return

        # Transaction fee for current accounts
        transaction_fee = 0
        if account_type == 'current':
            transaction_fee = amount * 0.01
            total_deduction = amount + transaction_fee
            if total_deduction > sender_balance[0][0]:
                print('Insufficient Balance to cover the transaction and fees. Please Deposit Money.')
                return
            amount = total_deduction  # Deduct the transaction fee from the sender's balance

        receiver_balance = db_query(f"SELECT balance FROM customers WHERE account_number = '{receive}';")
        if not receiver_balance:
            print("Account Number does not exist.")
            return

        updated_sender_balance = sender_balance[0][0] - amount
        updated_receiver_balance = receiver_balance[0][0] + (amount - transaction_fee)

        db_query(f"UPDATE customers SET balance = '{updated_sender_balance}' WHERE username = '{self.__username}';")
        db_query(f"UPDATE customers SET balance = '{updated_receiver_balance}' WHERE account_number = '{receive}';")

        receiver_username = db_query(f"SELECT username FROM customers WHERE account_number = '{receive}';")

        self.balanceequiry()
        db_query(f"INSERT INTO {receiver_username[0][0]}_transaction VALUES ("
                 f"'{datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Fund Transfer From {self.__account_number}',"
                 f"'{amount - transaction_fee}'"
                 f")")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Fund Transfer to {receive}',"
                 f"'{amount}'"
                 f")")

        if account_type == 'savings':
            self.__transaction_counts['transfers'] += 1
            db_query(
                f"UPDATE customers SET transfers_this_month = {self.__transaction_counts['transfers']} WHERE account_number = '{self.__account_number}';")

        print(
            f"{self.__username}, the amount has been successfully transferred from your account {self.__account_number}. Transaction fee applied: {transaction_fee if account_type == 'current' else 0}")


 # -----------------------------------------interest--------------------------------

    def get_account_type(self):
        result = db_query(f"SELECT account_type FROM customers WHERE account_number = '{self.__account_number}';")
        return result[0][0] if result else None

    def get_last_interest_date(self):
        result = db_query(f"SELECT last_interest_date FROM customers WHERE account_number = '{self.__account_number}';")
        print(result)
        return result[0][0] if result else None

    def update_last_interest_date(self, date):
        query = "UPDATE customers SET last_interest_date = %s WHERE account_number = %s"
        values = (date, self.__account_number)
        cursor.execute(query, values)
        mydb.commit()

    def calculate_interest(self):
        account_type = self.get_account_type()
        if account_type == 'savings':
            last_interest_date = self.get_last_interest_date()
            print(f'last_interest_date is  {last_interest_date}')

            current_date = date.today()
            print(f'current_date {current_date}')
            print(f'last_interest {last_interest_date}')

            if last_interest_date:
                months_passed = (current_date.year - last_interest_date.year) * 12 + (
                            current_date.month - last_interest_date.month)
                if months_passed >= 1:  # Check if at least one month has passed
                    interest_rate = 0.03  # 3% interest rate per month
                    result = db_query(
                        f"SELECT balance FROM customers WHERE account_number = '{self.__account_number}';")
                    balance = result[0][0]

                    # Calculate interest for each month passed
                    interest = balance * ((1 + interest_rate) ** months_passed - 1)
                    new_balance = balance + interest

                    update_query = "UPDATE customers SET balance = %s WHERE account_number = %s"
                    cursor.execute(update_query, (new_balance, self.__account_number))
                    mydb.commit()
                    self.update_last_interest_date(current_date)

                    print(f"Interest of {interest} added to your account.")
                    print(f'Now your bank balance is {new_balance}')
                else:
                    print("Interest not yet due.")
            else:
                print("Last interest date not found.")
        else:
            print("Your account is not a savings account")


def reset_limits_if_first_of_month(account_number):
    today = date.today()
    result = db_query(f"SELECT last_reset_date FROM customers WHERE account_number = '{account_number}';")
    if result:
        last_reset_date = result[0][0]
        if last_reset_date is None or (last_reset_date.month != today.month or last_reset_date.year != today.year):
            db_query(f"UPDATE customers SET withdrawals_this_month = 0, transfers_this_month = 0, last_reset_date = '{today}' WHERE account_number = '{account_number}';")
            mydb.commit()
