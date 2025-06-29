import requests
import json
import sys

# --- Configuration ---
# This is the default endpoint for Rasa Core's REST webhook.
# If your Rasa Core server is running on a different port or path, adjust this URL.
# The URL you provided (http://localhost:5055/webhook) is typically for the Rasa Action Server,
# not for sending user messages to Rasa Core for NLU/dialogue responses.
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

# A unique sender ID for this chat session.
# You can change this or make it dynamic if you need to distinguish users.
SENDER_ID = "test_user"

# --- Helper Function to Send Message to Rasa ---
def send_message_to_rasa(message: str) -> list:
    """
    Sends a user message to the Rasa bot and returns the bot's responses.

    Args:
        message (str): The user's message to send.

    Returns:
        list: A list of dictionaries, where each dictionary represents a bot response
              (e.g., {"text": "Hello!"}, {"image": "url_to_image"}).
              Returns an empty list if there's an error or no response.
    """
    payload = {
        "sender": SENDER_ID,
        "message": message
    }
    # payload = {
    #     "next_action": "action_get_weather",  # Example action name
    #     "tracker": {
    #         "sender_id": "test_user",
    #         "slots": {},
    #         "latest_message": {
    #             "intent": {
    #                 "name": "ask_weather",  # Example intent name
    #                 "confidence": 1.0
    #             },
    #             "entities": []
    #         },
    #         "events": [],
    #         "paused": False,
    #         "latest_input_channel": "rest",
    #         "latest_event_time": 0
    #     },
    #     "domain": {
    #         "intents": [
    #             {
    #                 "name": "ask_weather",  # Example intent name
    #                 "use_entities": True
    #             }
    #         ],
    #         "entities": [],
    #         "slots": {},
    #         "responses": {},
    #         "actions": ["action_get_weather"],  # Example action name
    #         "forms": {},
    #         "e2e_actions": []
    #     },
    #     "version": "3.1"
    # }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"\nSending message to Rasa: '{message}'")
    try:
        # Send the POST request to the Rasa API
        response = requests.post(RASA_API_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the JSON response
        rasa_responses = response.json()
        return rasa_responses

    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to Rasa server at {RASA_API_URL}.")
        print("Please ensure your Rasa Core server is running (e.g., `rasa run`).")
        return []
    except requests.exceptions.Timeout:
        print("❌ Error: Request to Rasa server timed out.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error from Rasa server: {e}")
        print(f"Response content: {response.text}")
        return []
    except json.JSONDecodeError:
        print("❌ Error: Could not decode JSON response from Rasa server.")
        print(f"Raw response: {response.text}")
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return []

# --- Main Chat Loop ---
def chat_with_rasa():
    """
    Starts an interactive chat session with the Rasa bot.
    """
    print("--- Rasa Chatbot ---")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("--------------------")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            bot_responses = send_message_to_rasa(user_input)

            if bot_responses:
                for response in bot_responses:
                    if "text" in response:
                        print(f"Bot: {response['text']}")
                    elif "image" in response:
                        print(f"Bot: [Image] {response['image']}")
                    # Add more handling for other response types (e.g., buttons, custom)
                    # For example:
                    # elif "buttons" in response:
                    #     print("Bot: Here are some options:")
                    #     for button in response["buttons"]:
                    #         print(f" - {button['title']} (payload: {button['payload']})")
                    # elif "custom" in response:
                    #     print(f"Bot: [Custom Response] {response['custom']}")
            else:
                print("Bot: (No response from Rasa or an error occurred.)")

        except KeyboardInterrupt:
            print("\nChat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred during chat: {e}")
            # Continue the loop even if an error occurs, unless it's critical

# --- Entry Point ---
if __name__ == "__main__":
    # Ensure 'requests' library is installed: pip install requests
    try:
        import requests
    except ImportError:
        print("Error: The 'requests' library is not installed.")
        print("Please install it using: pip install requests")
        sys.exit(1)

    chat_with_rasa()