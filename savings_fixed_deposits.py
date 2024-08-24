# savings_fixed_deposits.py

from database import cursor, mydb
from datetime import date, timedelta

class SavingsFixedDeposits:

    def __init__(self, account_number):
        self.__account_number = account_number

    def create_fixed_deposit(self, amount, months):
        if amount < 50000:
            print("Minimum deposit amount is ₹50,000.")
            return

        # Check if the user already has fixed deposits or not
        query = '''
                SELECT COUNT(*) 
                FROM fixed_deposits 
                WHERE account_number = %s AND status = 'active'
            '''
        cursor.execute(query, (self.__account_number,))
        active_deposits = cursor.fetchone()[0]

        if active_deposits > 0:
            print("You already have an active fixed deposit. You cannot create another one.")
            return

        maturity_date = date.today() + timedelta(days=30 * months)
        query = '''
            INSERT INTO fixed_deposits 
            (account_number, deposit_amount, deposit_date, maturity_date) 
            VALUES (%s, %s, %s, %s)
        '''
        values = (self.__account_number, amount, date.today(), maturity_date)
        cursor.execute(query, values)
        mydb.commit()
        print("Fixed deposit created successfully.")

    def check_and_add_fixed_deposit_interest(self):
        query = '''
            SELECT deposit_amount, maturity_date 
            FROM fixed_deposits 
            WHERE account_number = %s AND status = 'active'
        '''
        cursor.execute(query, (self.__account_number,))
        deposits = cursor.fetchall()

        for deposit in deposits:
            deposit_amount, maturity_date = deposit
            if date.today() >= maturity_date:
                # Calculate interest
                interest_rate = 0.03  # 3% monthly
                months_passed = (maturity_date.year - date.today().year) * 12 + (
                            maturity_date.month - date.today().month)
                interest = deposit_amount * ((1 + interest_rate) ** months_passed - 1)

                # Add interest to balance
                query = '''
                    UPDATE customers 
                    SET balance = balance + %s 
                    WHERE account_number = %s
                '''
                cursor.execute(query, (interest, self.__account_number))
                mydb.commit()

                # Update fixed deposit status
                query = '''
                    UPDATE fixed_deposits 
                    SET status = 'completed' 
                    WHERE account_number = %s AND deposit_date = %s
                '''
                cursor.execute(query, (self.__account_number, maturity_date))
                mydb.commit()

                print(f"Fixed deposit interest of ₹{interest:.2f} added to your account.")
            else:
                print("No fixed deposit interest due today.")

    def break_fixed_deposit(self):
        try:
            query = '''
                SELECT deposit_amount, deposit_date
                FROM fixed_deposits
                WHERE account_number = %s AND status = 'active'
            '''
            cursor.execute(query, (self.__account_number,))
            deposits = cursor.fetchall()

            print(f"Deposits found: {deposits}")  # Debug statement

            if not deposits:
                print("No active fixed deposits found.")
                return

            for deposit in deposits:
                deposit_amount, deposit_date = deposit

                # Return only the principal amount
                query = '''
                    UPDATE customers
                    SET balance = balance + %s
                    WHERE account_number = %s
                '''
                cursor.execute(query, (deposit_amount, self.__account_number))
                mydb.commit()

                # Update fixed deposit status
                query = '''
                    DELETE FROM fixed_deposits
                    WHERE account_number = %s AND deposit_date = %s
                '''
                cursor.execute(query, (self.__account_number, deposit_date))
                mydb.commit()

                print(f"Fixed deposit broken. Principal amount of ₹{deposit_amount} returned.")
        except Exception as e:
            print(f"Error breaking fixed deposit: {e}")

    def view_fixed_deposits(self):
        query = '''
            SELECT deposit_amount, deposit_date, maturity_date, status 
            FROM fixed_deposits 
            WHERE account_number = %s
        '''
        cursor.execute(query, (self.__account_number,))
        deposits = cursor.fetchall()

        if not deposits:
            print("No fixed deposits found.")
            return

        print("Fixed Deposits Details:")
        for deposit in deposits:
            deposit_amount, deposit_date, maturity_date, status = deposit
            print(f"Amount: ₹{deposit_amount}")
            print(f"Deposit Date: {deposit_date}")
            print(f"Maturity Date: {maturity_date}")
            print(f"Status: {status}")
            print("-" * 30)
