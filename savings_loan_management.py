from datetime import datetime

class LoanManagement:
    def __init__(self, cursor, mydb):
        self.cursor = cursor
        self.mydb = mydb

    def fetch_user_details(self):
        account_number = int(input("Enter your account number: "))
        account_type = input("Enter your account type (savings/checking): ")
        monthly_income = float(input("Enter your monthly income: "))
        has_property = input("Do you have private property (yes/no): ").strip().lower() == 'yes'
        property_documents = input("Do you agree to provide property documents (yes/no): ").strip().lower() == 'yes'
        loan_agreement = input(
            "Do you agree to the loan terms including property ownership in case of default (yes/no): ").strip().lower() == 'yes'

        return {
            'account_number': account_number,
            'account_type': account_type,
            'monthly_income': monthly_income,
            'has_property': has_property,
            'property_documents': property_documents,
            'loan_agreement': loan_agreement
        }

    # Function to apply for a loan
    def apply_for_loan(self):
        user_details = self.fetch_user_details()
        loan_amount = float(input("Enter the loan amount: "))

        if user_details['account_type'] != 'savings':
            return "Loan can only be applied to savings accounts."

        if user_details['monthly_income'] < (0.05 * loan_amount):
            return "Monthly income must be at least 5% of the loan amount."

        if not user_details['has_property']:
            return "User must have private property to apply for a loan."

        if not user_details['property_documents']:
            return "User must agree to provide property documents."

        if not user_details['loan_agreement']:
            return "User must agree to loan terms, including property ownership in case of default."

        # Taking input for due date
        due_date = None
        while True:
            due_date_input = input("Enter the loan due date (YYYY-MM-DD, maximum 10 years): ")
            try:
                due_date = datetime.strptime(due_date_input, '%Y-%m-%d').date()

                if due_date <= datetime.now().date():
                    print("Due date must be a future date.")
                    continue

                if (due_date - datetime.now().date()).days > 3650:  # 10 years
                    print("Due date cannot exceed 10 years from today.")
                    continue

                break  # Exit the loop if a valid date is entered

            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                continue

        print(f"Valid due date entered: {due_date}")

        # Calculate interest rate (e.g., 7% annual interest rate)
        interest_rate = 0.07
        loan_date = datetime.now().date()
        interest = loan_amount * interest_rate * ((due_date - loan_date).days / 365)
        total_repayment = loan_amount + interest

        # Insert loan into the database
        self.cursor.execute('''
            INSERT INTO loans (account_number, loan_amount, loan_date, due_date, balance_amount)
            VALUES (%s, %s, %s, %s, %s)
        ''', (user_details['account_number'], loan_amount, loan_date, due_date, total_repayment))
        self.mydb.commit()

        return "Loan application successful. Your loan details have been recorded."

    # Function to update loan amount when user makes a payment
    def make_payment(self, loan_id, payment_amount):
        self.cursor.execute('SELECT balance_amount FROM loans WHERE loan_id = %s AND status = "active"', (loan_id,))
        result = self.cursor.fetchone()

        if result:
            remaining_balance = result[0]
            if payment_amount > remaining_balance:
                return "Payment amount exceeds remaining balance."

            new_balance = remaining_balance - payment_amount
            if new_balance <= 0:
                self.cursor.execute('UPDATE loans SET balance_amount = 0, status = "closed" WHERE loan_id = %s', (loan_id,))
            else:
                self.cursor.execute('UPDATE loans SET balance_amount = %s WHERE loan_id = %s', (new_balance, loan_id))
            self.mydb.commit()
            return "Payment processed successfully."
        return "Loan not found or already closed."

    # Function to view loan details
    def view_loan_details(self):
        account_number = int(input("Enter your account number: "))
        self.cursor.execute('SELECT * FROM loans WHERE account_number = %s AND status = "active"', (account_number,))
        loans = self.cursor.fetchall()

        if not loans:
            return "No active loans found."

        print("Active Loans:")
        for loan in loans:
            loan_id, acc_num, loan_amount, loan_date, due_date, balance_amount, status = loan
            print(f"Loan ID: {loan_id}")
            print(f"Account Number: {acc_num}")
            print(f"Loan Amount: {loan_amount}")
            print(f"Loan Date: {loan_date}")
            print(f"Due Date: {due_date}")
            print(f"Remaining Balance: {balance_amount}")
            print(f"Status: {status}\n")

        return "Loan details displayed."
