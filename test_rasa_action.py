import requests
import json

def test_custom_action(action_name: str, intent_name: str):
    url = "http://localhost:5055/webhook"

    payload = {
        "next_action": action_name,
        "tracker": {
            "sender_id": "test_user",
            "slots": {},
            "latest_message": {
                "intent": {
                    "name": intent_name,
                    "confidence": 1.0
                },
                "entities": []
            },
            "events": [],
            "paused": False,
            "latest_input_channel": "rest",
            "latest_event_time": 0
        },
        "domain": {
            "intents": [
                {
                    "name": intent_name,
                    "use_entities": True
                }
            ],
            "entities": [],
            "slots": {},
            "responses": {},
            "actions": [action_name],
            "forms": {},
            "e2e_actions": []
        },
        "version": "3.1"
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print(f"Status Code: {response.status_code}")
    try:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=4))
    except:
        print("Response Text:")
        print(response.text)

# 🔹 Examples:
# test_custom_action("action_get_time", "ask_time")
test_custom_action("action_get_weather", "ask_weather")
# test_custom_action("action_get_location", "ask_location")
