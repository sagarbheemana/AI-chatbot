# AI Chatbot with Tool Routing, Memory, and Local LLM
Built using FastAPI, LangChain, Streamlit, and Ollama

## 1. Project Overview
This project is an AI-powered chatbot that runs locally using the Mistral model via Ollama. It includes:
- Semantic and keyword-based tool routing
- Conversation memory stored in JSON
- Mental wellness tools
- Student marks grading tool
- Real-time streaming chat responses
- FastAPI backend
- Streamlit UI interface
- Fully offline operation (no API key required)

## 2. Features

### AI Tools
1. positive_prompt – Generates motivational messages
2. negative_prompt – Reframes negative thoughts
3. student_marks – Creates grade and feedback reports
4. suicide_crisis_support – Provides emergency safety support

### Routing System
- Semantic routing using LangChain Agent
- Keyword routing using detect_tool()

### Memory System
- Saved in conversation_history.json
- Memory functions: save, load, list, delete conversations

### Streamlit Frontend
- Chat UI with live typing animation
- Sidebar for saved conversations
- Save/load/delete chats

### FastAPI Backend
- POST /chat
- GET /tools
- GET /health

### Local LLM (Ollama)
- Uses Mistral model offline
- No API key required

## 3. Project Structure

CHATBOT/
│── backend_api.py            # FastAPI backend + keyword routing  
│── tool_router.py            # Tools + agent + semantic routing  
│── streamlit_app.py          # Streamlit UI  
│── database.py               # Memory system  
│── conversation_history.json # Saved conversations  
│── requirements.txt          # Dependencies  
│── .gitignore

## 4. Installation Guide

Create Virtual Environment:
python -m venv .venv

Activate Virtual Environment:
& .venv/Scripts/Activate.ps1

Install Dependencies:
pip install -r requirements.txt
pip install langchain-ollama

## 5. Setup Ollama (Local LLM)

Start Ollama server:
ollama serve

Download Mistral model:
ollama pull mistral

(Optional) Test model:
ollama run mistral

## 6. Run FastAPI Backend

Start backend server:
uvicorn backend_api:app --host 0.0.0.0 --port 8000

Health check:
http://localhost:8000/health

Chat endpoint:
http://localhost:8000/chat

Tools endpoint:
http://localhost:8000/tools

## 7. Run Streamlit Frontend

Run UI:
streamlit run streamlit_app.py

UI opens at:
http://localhost:8501

## 8. Test Using Postman

POST URL:
http://localhost:8000/chat

Body → Raw → JSON:
{
  "query": "motivate me",
  "conversation_history": []
}

Example Response:
{
  "response": "You can achieve anything with focus.",
  "tool_used": "positive_prompt",
  "conversation_history": [...]
}

## 9. How the Chatbot Works Internally

1. User sends a message (Streamlit/Postman).
2. FastAPI receives message via /chat.
3. Backend forwards message to AI agent.
4. Semantic routing selects the correct tool.
5. Keyword routing double-checks for safety.
6. Tool executes and generates response.
7. Memory is saved in JSON.
8. Streamlit displays the answer with typing effect.
9. User can save, load, or delete chats.

## 10. Tool Descriptions

positive_prompt:
Returns motivational and encouraging responses.

negative_prompt:
Uses 5-step reframing to reduce stress/worry.

student_marks:
Takes marks and returns grade + feedback.

suicide_crisis_support:
Provides emergency help lines and safety steps.

## 11. Future Enhancements
- Use database instead of JSON
- Add login system
- Add more tools
- Add voice input/output support

## 12. System Architecture

USER (Frontend)
      │
      ▼
Streamlit UI (streamlit_app.py)
- Sends user messages to FastAPI
- Displays responses with typing effect
- Loads and saves past conversations
      │
      ▼
FastAPI Backend (backend_api.py)
- Receives user requests at /chat
- Applies keyword-based routing
- Forwards message + history to AI agent
      │
      ▼
AI Agent (tool_router.py)
- Local LLM (Mistral via Ollama)
- Semantic routing using system prompt
- Selects correct tool:
    • positive_prompt
    • negative_prompt
    • student_marks
    • suicide_crisis_support
- Generates response
      │
      ▼
Memory System (database.py)
- Saves conversation in JSON
- Loads previous conversations
- Lists all chats
- Deletes conversations
      │
      ▼
conversation_history.json
- Persistent storage of all chat histories

Local LLM Engine (Ollama)
- Runs Mistral model offline
- Processes natural language
- No API key required

Overall Flow:
User → Streamlit → FastAPI → AI Agent → Tool → Memory → Streamlit
