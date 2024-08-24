#DATABASE MANAGEMENT BANKING
import mysql.connector as sql

mydb = sql.connect(
    host = 'localhost',
    user = 'username',
    passwd = 'yourpassword',
    database = 'Bank'
)

# print('connection established')
# print(mydb)
cursor = mydb.cursor()


def db_query(str):
    cursor.execute(str)
    result = cursor.fetchall()
    return result

def createcustomertable():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers
                (username VARCHAR(20) NOT NULL,
                salt Binary(16) NOT NULL,
                password Binary(32) NOT NULL,
                name varchar(20) NOT NULL,
                age INTEGER NOT NULL,
                city VARCHAR(20) NOT NULL,
                balance INTEGER NOT NULL,
                account_number INTEGER NOT NULL,
                email Varchar(50) NOT NULL ,
                created_at DATETIME NOT NULL,
                status BOOLEAN NOT NULL,
                account_type VARCHAR(20) NOT NULL,
                last_interest_date DATE DEFAULT NULL,
                withdrawals_this_month INTEGER DEFAULT 0,
                transfers_this_month INTEGER DEFAULT 0,
                last_reset_date DATE DEFAULT NULL,
                PRIMARY KEY (account_number)
                )
    ''')

mydb.commit()


def create_archive_table():
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers_archive
                (username VARCHAR(20) NOT NULL,
                age INTEGER NOT NULL,
                city VARCHAR(20) NOT NULL,
                balance INTEGER NOT NULL,
                account_number INTEGER NOT NULL,
                email Varchar(50) NOT NULL ,
                deleted_at DATETIME NOT NULL,
                status BOOLEAN NOT NULL)
    ''')
mydb.commit()


def create_fixed_deposit_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fixed_deposits (
            account_number INTEGER NOT NULL,
            deposit_amount INTEGER NOT NULL,
            deposit_date DATE NOT NULL,
            maturity_date DATE NOT NULL,
            status ENUM('active', 'completed', 'broken') DEFAULT 'active',
            PRIMARY KEY (account_number, deposit_date)
        )
    ''')
mydb.commit()



def create_loans_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            loan_id INTEGER AUTO_INCREMENT PRIMARY KEY,
            account_number INTEGER NOT NULL,
            loan_amount INTEGER NOT NULL,
            loan_date DATE NOT NULL,
            due_date DATE NOT NULL,
            balance_amount INTEGER NOT NULL,
            status ENUM('active', 'closed') DEFAULT 'active',
            FOREIGN KEY (account_number) REFERENCES customers(account_number)
        )
    ''')
mydb.commit()


def create_corporate_loans_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS corporate_loans (
            loan_id INTEGER AUTO_INCREMENT PRIMARY KEY,
            account_number INTEGER NOT NULL,
            loan_amount INTEGER NOT NULL,
            loan_date DATE NOT NULL,
            due_date DATE NOT NULL,
            balance_amount INTEGER NOT NULL,
            status ENUM('active', 'closed') DEFAULT 'active',
            FOREIGN KEY (account_number) REFERENCES customers(account_number)
        )
    ''')
mydb.commit()

def create_feedback_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            feedback_text TEXT,
            feedback_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES customers(account_number)
        )
    ''')
mydb.commit()



def create_admin_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            salt Binary(16) NOT NULL,
            password Binary(32) NOT NULL,
            name VARCHAR(50) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            age INT NOT NULL,
            city VARCHAR(50) NOT NULL,
            nationality VARCHAR(50) NOT NULL,
            position_name VARCHAR(50) NOT NULL,
            working_status BOOLEAN NOT NULL,
            salary DECIMAL(10, 2) NOT NULL
        )
    ''')
mydb.commit()


if __name__ == "__main__":
    createcustomertable()
    create_archive_table()
    create_fixed_deposit_table()
    create_loans_table()
    create_corporate_loans_table()
    create_feedback_table()
    create_admin_table()
    # deletecustomertable()