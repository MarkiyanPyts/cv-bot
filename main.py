import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def main():
    print("Hello from cv-bot!")

    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": "Hello from cv-bot!",
        }
    )


if __name__ == "__main__":
    main()
