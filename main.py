from agents import Runner
from dotenv import load_dotenv
from my_agents import MyCVAvatar
import asyncio
from agents import trace

load_dotenv(override=True)

pdf_path = "me/Markiyan_Pyts_CV.pdf"
summary_path = "me/summary.txt"

async def main():
    cv_avatar = MyCVAvatar(name="Markiyan Pyts", pdf_path=pdf_path, summary_path=summary_path)

    with trace("Protected Automated SDR"):
        result = await Runner.run(cv_avatar.agent, "how long did you study?")
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
