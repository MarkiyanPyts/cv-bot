from pypdf import PdfReader
from templates import create_cv_agent_instructions
from my_tools import record_user_details, record_unknown_question, analyze_experience_duration
from agents import Agent

class MyCVAvatar():
    def __init__(self, name: str, pdf_path: str, summary_path: str):
        self.name = name
        
        reader = PdfReader(pdf_path)
        print(f"Loading PDF from: {pdf_path}")
        print(f"PDF has {len(reader.pages)} pages")
        self.cv = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.cv += text
        print(f"Loaded {len(self.cv)} characters from PDF")
        with open(summary_path, "r", encoding="utf-8") as f:
            self.summary = f.read()
        self.agent = self.create_agent()

    def create_agent(self):
        return Agent(
            name=self.name,
            instructions=create_cv_agent_instructions(name=self.name, summary=self.summary, cv=self.cv),
            model="gpt-4o-mini",
            tools=[record_user_details, record_unknown_question, analyze_experience_duration]
        )