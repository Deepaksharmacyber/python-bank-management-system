from prettytable import PrettyTable
from database import *  # Adjust this import based on how you connect to your database
from datetime import *
import datetime


class CustomerManagement:
    def __init__(self, cursor):
        self.cursor = cursor

    def view_all_customers(self):
        query = "SELECT account_number, username, email, name, age, city, account_type FROM customers"
        self.cursor.execute(query)
        customers = self.cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["Account Number", "Username", "Email", "Name", "Age", "City", "Account Type"]

        for customer in customers:
            table.add_row(customer)

        return table

    def view_customer_by_account_number(self, account_number):
        query = f"SELECT account_number, username, email, name, age, city, account_type FROM customers WHERE account_number = {account_number}"
        self.cursor.execute(query)
        customer = self.cursor.fetchone()

        table = PrettyTable()
        table.field_names = ["Account Number", "Username", "Email", "Name", "Age", "City", "Account Type"]

        if customer:
            table.add_row(customer)
        else:
            table.add_row(["No data found"] * len(table.field_names))

        return table

    def delete_customer_account(self, account_number):
        try:
            # Check if the customer has any active loans
            self.cursor.execute(f"""
                SELECT COUNT(*)
                FROM loans
                WHERE account_number = {account_number} AND status = 'active'
            """)
            active_loans_count = self.cursor.fetchone()[0]

            if active_loans_count > 0:
                return "Cannot delete account: The customer has active loans. Please close the loans first."

            # Delete associated feedback
            self.cursor.execute("""
                    DELETE FROM feedback WHERE user_id = %s
                """, (account_number,))
            mydb.commit()


            # Archive the customer data before deletion
            # customer_data = db_query(f"SELECT * from customers where account_number = '{account_number}';")
            query = f"""
                SELECT username, salt, password, name, age, city, balance, account_number, email, created_at, status 
                FROM customers 
                WHERE account_number = '{account_number}'
            """

            self.cursor.execute(query)
            customer_data = self.cursor.fetchone()

            if customer_data:
                # customer_data = customer_data[0]
                deleted_at = datetime.date.today()
                print('hi')
                username, salt, hashed_password, name, age, city, balance, account_number, email, inserted_at, status = customer_data
                print('hello')
                archive_query = f"""
                                        INSERT INTO customers_archive 
                                        (username, age, city, balance, account_number, email, deleted_at, status)
                                        VALUES ('{username}','{age}', '{city}', {balance}, {account_number}, '{email}', '{deleted_at}', {status});
                                        """
                cursor.execute(archive_query)
                mydb.commit()

                delete_query = f"DELETE from customers where username = '{username}';"
                cursor.execute(delete_query)
                mydb.commit()

                return "Customer account archived and deleted."
            else:
                return "Customer account not found."

        except Exception as e:
            return f"An error occurred: {str(e)}"

    def view_feedback(self):
        query = "SELECT user_id, feedback_text, feedback_date FROM feedback"
        self.cursor.execute(query)
        feedbacks = self.cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["User ID", "Feedback Text", "Feedback Date"]

        for feedback in feedbacks:
            table.add_row(feedback)

        return table
