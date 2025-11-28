# AI Chatbot with Tool Routing, Memory, and Local LLM
Built using FastAPI, LangChain, Streamlit, and Ollama

## 1. Project Overview
This project is an AI-powered chatbot that runs locally using the Mistral model via Ollama. It includes:
- Tool routing (semantic + keyword)
- Conversation memory stored in JSON
- Mental wellness support tools
- Student marks grading tool
- Real-time streaming chat responses
- FastAPI backend for API usage
- Streamlit UI interface
- Fully offline operation (no API key required)

## 2. Features

### AI Tools
1. positive_prompt – Generates motivational messages
2. negative_prompt – Reframes negative thoughts
3. student_marks – Creates grade + feedback reports
4. suicide_crisis_support – Provides emergency help and safety instructions

### Routing
- Semantic routing using LangChain Agent
- Keyword routing using detect_tool() in FastAPI

### Memory System
- Stored in conversation_history.json
- Functions include: save, load, list, and delete conversation

### Streamlit Frontend
- Chat interface with live typing effect
- Sidebar for past conversations
- Save/load/delete chat options

### FastAPI Backend
- POST /chat
- GET /tools
- GET /health

### Local LLM (Ollama)
- Uses the Mistral model
- Runs offline
- No API key required

## 3. Project Structure

CHATBOT/
│── backend_api.py            # FastAPI backend + keyword routing
│── tool_router.py            # Tools + LLM agent + semantic routing
│── streamlit_app.py          # Streamlit UI with streaming features
│── database.py               # Memory handling system
│── conversation_history.json # Chat memory storage
│── requirements.txt          # Python dependencies
│── .gitignore

## 4. Installation Guide

Create Virtual Environment:
python -m venv .venv

Activate Virtual Environment (Windows PowerShell):
& .venv/Scripts/Activate.ps1

Install Dependencies:
pip install -r requirements.txt
pip install langchain-ollama

## 5. Setup Ollama (Local LLM)

Start Ollama server:
ollama serve

Download the Mistral model:
ollama pull mistral

(Optional) Test the model:
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

POST request URL:
http://localhost:8000/chat

Body (raw JSON):
{
  "query": "motivate me",
  "conversation_history": []
}

Example output:
{
  "response": "You can do it!",
  "tool_used": "positive_prompt",
  "conversation_history": [...]
}

## 9. How the Chatbot Works Internally

1. User sends a message from Streamlit or Postman.
2. FastAPI receives the message at /chat.
3. Backend sends the text to the AI agent (tool_router.py).
4. Semantic routing chooses the correct tool.
5. Keyword routing double-checks for safety or academic queries.
6. Tool generates correct response.
7. Memory is saved in conversation_history.json.
8. Streamlit displays the reply in real-time typing style.
9. User can save, load, or delete conversations.

## 10. Tool Descriptions

positive_prompt:
Returns encouraging and motivational responses.

negative_prompt:
Provides a structured 5-step reframing for stress/worry.

student_marks:
Grades marks and returns feedback.

suicide_crisis_support:
Provides emergency helpline and safety directions.

## 11. Future Enhancements
- Replace JSON memory with a database
- Add user authentication
- Add more tools
- Voice assistant integration

## 12. Author
Sagar Gowd
Academic and learning project.
