from agents import function_tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@function_tool
def send_notification(email: str, name: str = "Name not provided", notes: str = "not provided"):
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": "Hello from cv-bot!",
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to send notification: {response.text}")
    print(f"Notification sent successfully to {email} for {name}. Notes: {notes}")

    return {"status": "success"}