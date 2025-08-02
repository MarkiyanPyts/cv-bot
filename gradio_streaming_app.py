import gradio as gr
from agents import Runner
from dotenv import load_dotenv
from my_agents import MyCVAvatar
import asyncio
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(override=True)

pdf_path = "me/Markiyan_Pyts_CV.pdf"
summary_path = "me/summary.txt"

# Initialize the CV avatar
cv_avatar = MyCVAvatar(name="Markiyan Pyts", pdf_path=pdf_path, summary_path=summary_path)

async def chat_with_cv_bot_streaming(message, history):
    """Process user message and stream bot response"""
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
        
        # Run the agent with streaming
        result = Runner.run_streamed(cv_avatar.agent, full_context)
        
        # Stream the response
        response_text = ""
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                chunk = event.data.delta
                response_text += chunk
                yield response_text
        
        # The final response is already accumulated in response_text
        # If we didn't get any streaming events, get the final output
        if not response_text:
            # Get the result without streaming as fallback
            non_streaming_result = await Runner.run(cv_avatar.agent, full_context)
            yield non_streaming_result.final_output
            
    except Exception as e:
        yield f"Error: {str(e)}"

def gradio_chat_streaming(message, history):
    """Wrapper to run async streaming function in sync context"""
    async def stream_wrapper():
        async for response in chat_with_cv_bot_streaming(message, history):
            yield response
    
    # Run the async generator
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        gen = stream_wrapper()
        while True:
            try:
                response = loop.run_until_complete(gen.__anext__())
                yield response
            except StopAsyncIteration:
                break
    finally:
        loop.close()

# Create Gradio interface with streaming
demo = gr.ChatInterface(
    fn=gradio_chat_streaming,
    chatbot=gr.Chatbot(show_label=False),
    theme=gr.themes.Soft(),
    css="main { padding: 5px !important; } input, textarea { font-size: 16px !important; } .input-container { display: flex !important; gap: 10px !important; }"
)


if __name__ == "__main__":
    demo.launch(show_api=False)