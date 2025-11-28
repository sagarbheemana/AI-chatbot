from fastapi import FastAPI
from pydantic import BaseModel
from tool_router import create_chatbot_agent, process_message
import uvicorn

app = FastAPI(title="AI Chatbot API")

class QueryRequest(BaseModel):
    query: str
    conversation_history: list = []

class QueryResponse(BaseModel):
    response: str
    tool_used: str
    conversation_history: list

agent = create_chatbot_agent()

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    """Chat endpoint with tool routing."""
    response, history = process_message(
        agent,
        request.query,
        request.conversation_history
    )
    
    # Detect which tool was used
    tool_used = detect_tool(request.query)
    
    return QueryResponse(
        response=response,
        tool_used=tool_used,
        conversation_history=history
    )

def detect_tool(query: str) -> str:
    """Detect which tool was triggered."""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["motivate", "encourage", "inspire", "confident"]):
        return "positive_prompt"
    elif any(word in query_lower for word in ["worried", "anxious", "doubt", "fear"]):
        return "negative_prompt"
    elif any(word in query_lower for word in ["score", "mark", "grade", "exam"]):
        return "student_marks"
    elif any(word in query_lower for word in ["die", "suicide", "harm", "kill"]):
        return "suicide_crisis_support"
    else:
        return "general_response"

@app.get("/tools")
async def get_tools():
    """List all available tools."""
    return {
        "tools": [
            {"name": "positive_prompt", "description": "Motivation & encouragement"},
            {"name": "negative_prompt", "description": "Reframe negative thoughts"},
            {"name": "student_marks", "description": "Record grades & feedback"},
            {"name": "suicide_crisis_support", "description": "Crisis resources"}
        ]
    }

@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)