from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import uvicorn

app = FastAPI(
    title="Rasa-FastAPI Integration",
    description="API endpoints to send and receive messages from Rasa.",
    version="1.0.0"
)

RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

class RasaWebhookMessage(BaseModel):
    sender_id: str
    message: str

class SendMessageToRasa(BaseModel):
    sender: str
    message: str

@app.post("/rasa-webhook", status_code=200)
async def receive_from_rasa(message: RasaWebhookMessage):
    print(f"Received message from Rasa for sender '{message.sender_id}': {message.message}")
    return {"status": "success", "message": "Message received and processed."}

@app.post("/send-to-rasa", status_code=200)
async def send_message_to_rasa(message_data: SendMessageToRasa):
    payload = {
        "sender": message_data.sender,
        "message": message_data.message
    }
    print(f"Sending message to Rasa for sender '{message_data.sender}': {message_data.message}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(RASA_SERVER_URL, json=payload, timeout=60.0)

        response.raise_for_status()
        rasa_response = response.json()

        print(f"Rasa response: {rasa_response}")
        return {"status": "success", "rasa_response": rasa_response}

    except httpx.RequestError as exc:
        print(f"An error occurred while requesting Rasa server: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Could not connect to Rasa server: {exc}"
        )
    except httpx.HTTPStatusError as exc:
        print(f"Rasa server returned an error: {exc.response.status_code} - {exc.response.text}")
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Rasa server error: {exc.response.text}"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)