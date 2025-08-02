import gradio as gr
from agents import Runner
from dotenv import load_dotenv
from my_agents import MyCVAvatar
import asyncio

load_dotenv(override=True)

pdf_path = "me/Markiyan_Pyts_CV.pdf"
summary_path = "me/summary.txt"

# Initialize the CV avatar
cv_avatar = MyCVAvatar(name="Markiyan Pyts", pdf_path=pdf_path, summary_path=summary_path)

async def chat_with_cv_bot(message, history):
    """Process user message and return bot response"""
    try:
        # Build conversation context from history
        conversation = []
        for user_msg, assistant_msg in history:
            conversation.append(f"User: {user_msg}")
            conversation.append(f"Assistant: {assistant_msg}")
        
        # Add current message
        conversation.append(f"User: {message}")
        
        # Join all messages into a single context string
        full_context = "\n".join(conversation)
        
        # Run the agent with the full conversation context
        result = await Runner.run(cv_avatar.agent, full_context)
        # Extract only the final output string from RunResult
        # The final_output attribute contains the actual response text
        return result.final_output
    except Exception as e:
        return f"Error: {str(e)}"

def gradio_chat(message, history):
    """Wrapper to run async function in sync context"""
    response = asyncio.run(chat_with_cv_bot(message, history))
    return response

# Create Gradio interface
demo = gr.ChatInterface(
    fn=gradio_chat,
    title="CV Bot - Chat with Markiyan's Resume",
    description="Ask me anything about Markiyan's professional experience, skills, and background!",
    examples=[
        "What is Markiyan's professional experience?",
        "What programming languages does Markiyan know?",
        "Tell me about Markiyan's education",
        "What projects has Markiyan worked on?",
        "How long did Markiyan work at his previous companies?"
    ],
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    demo.launch()