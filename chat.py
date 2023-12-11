import pandas as pd
from dotenv import load_dotenv
import os

# load env
load_dotenv()

# set api key
api_key = os.getenv("OPENAI_API_KEY")

# Check if running in GitHub Actions and use the secret if available
if "GITHUB_ACTIONS" in os.environ:
    api_key = os.getenv("INPUT_OPENAI_API_KEY")

# load dataset
url = "https://raw.githubusercontent.com/erijmo/ChatBot/main/healthcare_dataset.csv"
df = pd.read_csv(url)

def get_healthcare_response(user_input, user_name, df):
    # search for keyword in user input
    for column in df.columns:
        if column.lower() in user_input:
            response = f"{user_name}, your {column.lower()} is {df[column].iloc[0]}"
            return response

    # if no keyword located, ask for clarification
    return "I'm sorry, I couldn't understand your request. Can you please provide more details?"

# prompt response
print("HealthcareBot: Hello! I'm your HealthcareBot. May I know your name, please?")

while True:
    user_name = input("User: ")

    # check if the user's name is in the system
    if user_name.lower() in df["Name"].str.lower().values:
        print(f"HealthcareBot: Thank you, {user_name}! How can I assist you today?")
        break
    else:
        print("HealthcareBot: I'm sorry, but I couldn't find your name in the system. Please try again.")

# user interaction loop
while True:
    user_input = input("User: ")

    # check if any exit-related keywords are present in the user input
    if any(keyword in user_input.lower() for keyword in ['exit', 'bye', 'quit']):
        print("HealthcareBot: Goodbye! If you have more questions, feel free to ask.")
        break

    response = get_healthcare_response(user_input, user_name, df)
    if response:
        print("HealthcareBot:", response)
