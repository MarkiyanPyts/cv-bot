from agents import function_tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@function_tool
def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided"):
    """Use this tool to record that a user is interested in being in touch and provided an email address"""

    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": f"Someone with mail {email} and name {name} has the following notes: {notes}",
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to send notification: {response.text}")
    print(f"Notification sent successfully to {email} for {name}. Notes: {notes}")

    return {"status": "success"}

@function_tool
def record_unknown_question(question: str):
    """
    Always use this tool to record any question that couldn't be answered as you didn't know the answer
    """
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": f"Unknown question received: {question}",
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to send notification: {response.text}")
    print(f"Notification sent successfully for unknown question: {question}")

    return {"status": "success"}