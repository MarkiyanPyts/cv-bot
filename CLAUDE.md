# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a CV Bot - an AI-powered chatbot that represents a CV/resume as an interactive avatar. Built with Gradio and OpenAI Agents, it allows users to ask questions about professional experience and background.

## Development Commands

### Environment Setup
```bash
# Install dependencies with uv (Python 3.12+ required)
uv pip install -r requirements.txt

# Or install from pyproject.toml
uv pip install -e .
```

### Running the Application
```bash
# Run the streaming version (recommended)
uv run python gradio_streaming_app.py

# Run the non-streaming version
uv run python gradio_app.py

# Test the agent via CLI
uv run python main.py
```

### Deployment
```bash
# Compile requirements for Hugging Face deployment
uv pip compile pyproject.toml -o requirements.txt

# Deploy to Hugging Face Spaces
uv run gradio deploy
```

## Architecture Overview

### Core Components

1. **Agent System** (`my_agents.py`)
   - `MyCVAvatar` class creates the AI agent
   - Loads CV from PDF (`me/Markiyan_Pyts_CV.pdf`) and summary from text (`me/summary.txt`)
   - Uses GPT-4o-mini model with custom instructions from `templates.py`

2. **Custom Tools** (`my_tools.py`)
   - `record_user_details`: Captures interested user contact info
   - `record_unknown_question`: Logs unanswered questions
   - `analyze_experience_duration`: Calculates work experience durations
   - Sends notifications via Pushover API

3. **Web Interfaces**
   - `gradio_streaming_app.py`: Streaming chat interface with real-time responses
   - `gradio_app.py`: Standard chat interface
   - Both maintain conversation history in session state

4. **Templates** (`templates.py`)
   - `create_instructions()`: Generates detailed agent behavior instructions
   - Includes CV content, current date context, and professional guidelines

### Key Design Patterns

- **Session Management**: Each Gradio session maintains independent conversation history
- **Tool Integration**: Agent uses custom tools for specific tasks (contact recording, duration calculations)
- **Error Handling**: Basic try-catch for agent creation and message processing
- **Environment Variables**: Sensitive data (API keys) stored in `.env` file

### Data Flow

1. User enters question in Gradio interface
2. Question + conversation history sent to agent
3. Agent processes using CV content and custom tools
4. Response streamed back (or returned) to UI
5. Conversation history updated
6. Any user details or unknown questions recorded via tools

## Environment Variables

Required in `.env` file:
- `PUSHOVER_TOKEN`: For notification service
- `PUSHOVER_USER`: For notification recipient
- OpenAI API credentials (check agent initialization)

## Important Notes

- The CV PDF and summary files in `me/` directory are the source of truth for the agent's knowledge
- When modifying agent behavior, update `templates.py` rather than hardcoding in agent creation
- The streaming version (`gradio_streaming_app.py`) provides better UX for longer responses
- All user interactions can trigger notifications via Pushover (see `my_tools.py`)