from register import *
from admin_register import *
from bank import *
from archive_delete_customer import *
from change_details import *
from current_loan_management import *
from savings_loan_management import *
from savings_fixed_deposits import SavingsFixedDeposits
from currency_exchange import CurrencyExchange
from user_feedback import UserFeedback
from customer_management import *

status = False
admin_status = False
user = None
admin_user = None
print('Welcome to Sharma banking system')

while True:
    try:
        register = int(input("1. for Customer Signup\n"
                             "2. for Customer Signin\n"
                             "3. for Admin Signin\n"))
        if register in [1, 2, 3]:
            if register == 1:
                SignUp()
            elif register == 2:
                user = SignIn()
                status = True
                break
            elif register == 3:
                admin_user = AdminSignIn()
                admin_status = True
                break
        else:
            print('Please enter valid input from options')
    except ValueError:
        print('Invalid input, try again')

if status:
    if register == 2:
        # Customer functionalities
        account_number = db_query(
            f"SELECT account_number FROM customers WHERE username = '{user}';")
        reset_limits_if_first_of_month(account_number)
        currency_exchanger = CurrencyExchange(api_key='4592ef4ada82194a6843f41f')
        account_type = db_query(f"SELECT account_type FROM customers WHERE username = '{user}';")[0][0]
        loan_mgmt = LoanManagement(cursor, mydb) if account_type == 'savings' else CorporateLoanManagement(cursor, mydb)
        fixed_deposits = SavingsFixedDeposits(account_number[0][0])
        user_feedback = UserFeedback(account_number[0][0])

        while status:
            print(f"Welcome {user.capitalize()} Choose Your Banking Service\n")
            try:
                facility = int(input("1. Balance Enquiry\n"
                                     "2. Cash Deposit\n"
                                     "3. Cash Withdraw\n"
                                     "4. Fund Transfer\n"
                                     "5. Change my details\n"
                                     "6. Delete your account\n"
                                     "7. View Transactions\n"
                                     "8. Check interest rate\n"
                                     "9. Create Fixed Deposit\n"
                                     "10. Break Fixed Deposit\n"
                                     "11. View Fixed Deposits\n"
                                     "12. Apply for Loan\n"
                                     "13. Make Loan Payment\n"
                                     "14. View Loan Details\n"
                                     "15. Currency Exchange\n"
                                     "16. Submit Feedback\n"
                                     "17. Exit"))
                print(f'facility is {facility}')
                if facility >= 1 and facility <= 17:
                    if facility == 1:
                        bobj = Bank(user, account_number[0][0])
                        bobj.balanceequiry()

                    elif facility == 2:
                        while True:
                            try:
                                amount = int(input("Enter Amount to Deposit"))
                                bobj = Bank(user, account_number[0][0])
                                bobj.deposit(amount)
                                mydb.commit()
                                break
                            except ValueError:
                                print("Enter Valid Input ie. Number")
                                continue

                    elif facility == 3:
                        while True:
                            try:
                                # amount = int(input("Enter Amount to Withdraw"))
                                bobj = Bank(user, account_number[0][0])
                                bobj.withdraw()
                                mydb.commit()
                                break
                            except ValueError:
                                print("Enter Valid Input ie. Number")
                                continue
                    elif facility == 4:
                        while True:
                            try:
                                receive = int(input("Enter Receiver Account Number"))
                                amount = int(input("Enter Money to Transfer"))
                                bobj = Bank(user, account_number[0][0])
                                bobj.fundtransfer(receive, amount)
                                mydb.commit()
                                break
                            except ValueError:
                                print("Enter Valid Input ie. Number")
                                continue
                    elif facility == 5:
                        while True:
                            try:
                                det = (input("name \n"
                                             "age\n"
                                             "city\n"
                                             "email\n")).lower()
                                if det in ['name', 'age', 'email', 'city']:
                                    change_details(det)
                                    break
                                else:
                                    print('please enter valid input')
                            except ValueError:
                                print("Enter Valid Input ie. Number")
                    elif facility == 6:
                        while True:
                            archive_and_delete_customer()
                            status = False
                            break
                    elif facility == 7:
                        while True:
                            bobj = Bank(user, account_number[0][0])
                            bobj.view_transactions()
                            break
                    elif facility == 8:
                        while True:
                            bobj = Bank(user, account_number[0][0])
                            bobj.calculate_interest()  # Call the interest calculation function
                            print('hello')
                            mydb.commit()
                            break

                    elif facility == 9:
                        while True:
                            try:
                                amount = int(input("Enter amount for fixed deposit (minimum ₹50,000): "))
                                months = int(input("Enter number of months for the deposit: "))
                                fixed_deposits.create_fixed_deposit(amount, months)
                                break
                            except ValueError:
                                print("Enter Valid Input (Number).")

                    elif facility == 10:
                        fixed_deposits.break_fixed_deposit()

                    elif facility == 11:
                        fixed_deposits.view_fixed_deposits()

                    elif facility == 12:
                        while True:
                            result = loan_mgmt.apply_for_loan()
                            print(result)
                            break

                    elif facility == 13:
                        while True:
                            try:
                                loan_id = int(input("Enter your Loan ID: "))
                                payment_amount = float(input("Enter Payment Amount: "))
                                result = loan_mgmt.make_payment(loan_id, payment_amount)
                                print(result)
                                mydb.commit()
                                break
                            except ValueError:
                                print("Enter valid input (number).")
                                continue

                    elif facility == 14:
                        while True:
                            result = loan_mgmt.view_loan_details()
                            print(result)
                            break

                    if facility == 15:
                        source_currency = input('Enter the source currency e.g INR: ').upper()
                        target_currency = input('Enter the target currency e.g USD: ').upper()
                        try:
                            amount = float(input('Enter the amount: '))
                            currency_exchanger.display_conversion(source_currency, target_currency, amount)
                        except ValueError:
                            print("Enter a valid amount.")
                        continue

                    elif facility == 16:
                        feedback_text = input("Enter your feedback: ")
                        print(account_number[0][0])
                        user_feedback.submit_feedback(feedback_text)

                    elif facility == 17:
                        print("Thanks For Using Banking Services")
                        status = False
                        break

            except ValueError:
                print("Invalid Input Try Again with Numbers")
                continue

elif admin_status:
    customer_management = CustomerManagement(cursor)
    # Admin functionalities
    while admin_status:
        try:
            facility = int(input("1. View all customers\n"
                                 "2. View customer by account number\n"
                                 "3. Delete customer account\n"
                                 "4. View feedback\n"
                                 "5. Exit"))
            if facility == 1:
                # View all customers
                customers = customer_management.view_all_customers()  # Use the method from CustomerManagement class
                for customer in customers:
                    print(customer)

            elif facility == 2:
                # View customer by account number
                account_number = int(input("Enter customer account number: "))
                customer_table = customer_management.view_customer_by_account_number(account_number)
                print(customer_table)

            elif facility == 3:
                # Delete customer account
                account_number = int(input("Enter customer account number to delete: "))
                result = customer_management.delete_customer_account(account_number)
                print(result)

            elif facility == 4:
                # View feedback
                feedback_table = customer_management.view_feedback()
                print(feedback_table)

            elif facility == 5:
                print("Exiting admin services")
                admin_status = False
            else:
                print("Invalid input, try again")

        except ValueError:
            print("Invalid input, try again")



