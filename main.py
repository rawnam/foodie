import os
import sqlite3
from datetime import datetime
from langchain.chat_models import ChatOpenAI
import my_key

os.environ["OPENAI_API_KEY"] = my_key.get_key()

# Initialize the chat model
llm = ChatOpenAI(model_name=my_key.get_model())

# Connect to SQLite database
conn = sqlite3.connect('eating_habits.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS eating_habits (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        food TEXT,
        date TEXT
    )
''')

# Function to save data to database
def save_to_db(user_id, food, date):
    c.execute("INSERT INTO eating_habits (user_id, food, date) VALUES (?, ?, ?)", (user_id, food, date))
    conn.commit()

# Function to interact with user
def interact_with_user(user_id):
    # Ask the user what they ate today
    question = "Hello! What did you eat today?"
    print(question)
    food = input()

    # Save the data to the database
    save_to_db(user_id, food, datetime.now().strftime("%Y-%m-%d"))

    # Ask the user if they want to add more
    question = "Would you like to add more foods that you ate today? (yes/no)"
    print(question)
    response = input()

    while response.lower() == 'yes':
        question = "What else did you eat today?"
        print(question)
        food = input()

        # Save the data to the database
        save_to_db(user_id, food, datetime.now().strftime("%Y-%m-%d"))

        question = "Would you like to add more foods that you ate today? (yes/no)"
        print(question)
        response = input()

    print("Thank you for sharing your eating habits with us today!")

# Interact with user
interact_with_user('user_001')

# Close the database connection
conn.close()
