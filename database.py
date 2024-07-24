#DATABASE MANAGEMENT BANKING
import mysql.connector as sql

mydb = sql.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mysql123deepak',
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
                password VARCHAR(20) NOT NULL,
                name varchar(20) NOT NULL,
                age INTEGER NOT NULL,
                city VARCHAR(20) NOT NULL,
                balance INTEGER NOT NULL,
                account_number INTEGER NOT NULL,
                status BOOLEAN NOT NULL)
    ''')

mydb.commit()

# def delete_customer(username):
#     delete_query = f"DELETE FROM customers WHERE username = '{username}';"
#     cursor.execute(delete_query)
#     mydb.commit()
#     print(f"Customer with username '{username}' has been deleted.")
#
# delete_customer('deepak123')



if __name__ == "__main__":
    createcustomertable()