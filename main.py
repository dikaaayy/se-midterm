import requests
import os
from dotenv import load_dotenv

# Load the API key from .env file
load_dotenv()


# API endpoint and get API key from .env file
url = "https://api.openai.com/v1/chat/completions"
apiKey = os.getenv('API_KEY')

# Initial message to send to the API
# message = "Hello, how can I help you today?"

# History array to store the conversation context
history = []


def api_call(content, history):

    # JSON data to send to the API
    data = {
        "model": "gpt-3.5-turbo",
        "messages": history + [
            {
                "role": "user",
                "content": content
            }
        ]
    }

    # Because we're using REST API, we need to set the headers for authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apiKey}"
    }

    # Make the API call
    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        # Print the response from the API
        for choice in response_json["choices"]:
            print("\nChatGPT: " + choice["message"]["content"] + "\n")
            history.append({"role": "assistant", "content": choice["message"]["content"]})

    except Exception as e:
        print(f"Error: {e}")



# Keep asking for user input until they type "quit"
while True:

    # Get user input
    user_input = input("You: ")

    # Exit if user types "quit"
    if user_input.lower() == "quit" or user_input.lower() == "exit" or user_input.lower() == "q":
        break

    #Reset history if user types "reset"
    if user_input.lower() == "reset":
        history = []
        print("\nHistory has been wiped.\n")
        continue

    # Add user input to history
    history.append({"role": "user", "content": user_input})

    # Call the API
    api_call(user_input, history)


print("\nBye!")