from agents import function_tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()

@function_tool
def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> dict:
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
def record_unknown_question(question: str) -> dict:
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

@function_tool
def analyze_experience_duration(start_year: int, end_year: int) -> dict:
    """
    Analyzes the duration of experience between two dates.
    If user asks question about experience duration e.g 'how many years of experience you have as SA analise CV'  for all positions related to SA role and use start year of latest position as start_year and end year of newest related position as end_year parameter.

    If end year is not provided in cv for this position, use current year as end_year.
    """

    if start_year > end_year:
        raise ValueError("Start year cannot be greater than end year")

    duration = end_year - start_year
    print(f"Calculated experience duration: {duration} years from {start_year} to {end_year}")

    return {"experience_duration": duration, "start_year": start_year, "end_year": end_year}


