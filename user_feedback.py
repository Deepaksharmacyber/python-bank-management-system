from database import *

class UserFeedback:
    def __init__(self, user_id):
        self.user_id = user_id

    def submit_feedback(self, feedback_text):
        query = "INSERT INTO feedback (user_id, feedback_text) VALUES (%s, %s)"
        values = (self.user_id, feedback_text)
        print("Values:", values)
        cursor.execute(query, values)
        mydb.commit()
        print("Thank you for your feedback!")

    def view_all_feedback(self):
        query = "SELECT feedback.id, customers.username, feedback.feedback_text, feedback.feedback_date FROM feedback JOIN customers ON feedback.user_id = customers.account_number"
        cursor.execute(query)
        results = cursor.fetchall()
        for feedback in results:
            print(f"ID: {feedback[0]}, User: {feedback[1]}, Date: {feedback[3]}\nFeedback: {feedback[2]}\n")

# if __name__ == "__main__":
#     user_feedback = UserFeedback(1)  # Replace with actual user ID
#     user_feedback.submit_feedback("This is a feedback text.")
#     user_feedback.view_all_feedback()
