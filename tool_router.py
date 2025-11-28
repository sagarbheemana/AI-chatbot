# ============ IMPORTS ============
from langchain.tools import tool  # Decorator to create tools
from langchain_ollama import ChatOllama  # Local LLM from Ollama
from langchain.agents import create_agent  # Create AI agent
from langchain.messages import HumanMessage, AIMessage  # Message types
import os  # For environment variables
from dotenv import load_dotenv  # Load .env file

# Load environment variables from .env file
load_dotenv()

# ============ TOOL 1: POSITIVE PROMPT ============
@tool
def positive_prompt(topic: str, tone: str = "encouraging") -> str:
    """Generate positive, uplifting prompts for motivation and growth."""
    
    # Dictionary of motivational templates for different topics
    templates = {
        "self-improvement": f"You have unlimited potential. What one change can you make today? Stay {tone}!",
        "learning": f"Every expert was once a beginner. Keep a {tone} attitude!",
        "career": f"Your journey is unique. Focus on strengths. Stay {tone}!",
        "health": f"Your wellbeing matters. Stay {tone}!",
        "default": f"You are capable. Stay {tone}!"
    }
    
    # Get template for topic, use default if not found
    prompt = templates.get(topic.lower(), templates['default'])
    
    # Return formatted response with emoji
    return f"✨ {prompt}"

# ============ TOOL 2: NEGATIVE PROMPT ============
@tool
def negative_prompt(concern: str, context: str = "general") -> str:
    """Reframe negative thoughts with balanced perspective."""
    
    # Return structured response for addressing negative thoughts
    return f"""⚠️ Thought: {concern}
BALANCED VIEW:
1. Acknowledge - Valid
2. Question - Facts or assumptions?
3. Evidence - What contradicts this?
4. Reframe - Catastrophizing?
5. Action - One step?
You can handle this. You have support."""

# ============ TOOL 3: STUDENT MARKS ============
@tool
def student_marks(student_name: str, subject: str, marks: int) -> str:
    """Record grades and provide feedback."""
    
    # Grade assignment logic based on marks
    if marks >= 90:
        grade, feedback = "A+", "Excellent!"
    elif marks >= 80:
        grade, feedback = "A", "Very Good!"
    elif marks >= 70:
        grade, feedback = "B", "Good!"
    elif marks >= 60:
        grade, feedback = "C", "Satisfactory"
    elif marks >= 50:
        grade, feedback = "D", "Need Help"
    else:
        grade, feedback = "F", "Support Needed"
    
    # Return formatted grade report
    return f"📊 {student_name} - {subject}: {marks}/100\nGrade: {grade}\nFeedback: {feedback}\nNext: Practice & Review"

# ============ TOOL 4: CRISIS SUPPORT ============
@tool
def suicide_crisis_support() -> str:
    """Crisis resources and immediate help."""
    
    # Return crisis support information with hotlines and resources
    return """🆘 YOU ARE NOT ALONE

CALL NOW:
🇺🇸 988 | 🇬🇧 116123 | 🇮🇳 +91-22-2754-6669 | 🇦🇺 131114
TEXT: Crisis Text Line - Text HOME to 741741
GO TO ER IF IN DANGER

COPING:
• 5-4-3-2-1 grounding (see, touch, hear, smell, taste)
• Cold shower
• Exercise
• Call someone
• Eat & hydrate

RESOURCES:
suicidepreventionlifeline.org
findahelpline.com
7cups.com

YOUR LIFE MATTERS 💙
Get help NOW."""

# ============ CREATE AGENT ============
def create_chatbot_agent():
    """Create agent with Ollama (local LLM - no API key needed)."""
    
    # Initialize local Ollama LLM
    # base_url points to local Ollama server running on port 11434
    llm = ChatOllama(
        model="mistral",  # Use Mistral model (fast and accurate)
        base_url="http://localhost:11434",  # Local Ollama server
        temperature=0.3,  # Lower = more focused responses
        num_predict=300  # Limit response length (tokens)
    )
    
    # Create list of all available tools
    tools = [positive_prompt, negative_prompt, student_marks, suicide_crisis_support]
    
    # Create agent with LLM and tools bound
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""Help with mental wellness and academics. Be concise.

ROUTING:
- motivation → positive_prompt
- worries → negative_prompt  
- grades → student_marks
- crisis → suicide_crisis_support (IMMEDIATE)"""
    )
    
    return agent

# ============ PROCESS MESSAGE ============
def process_message_streaming(agent, user_message: str, conversation_history: list):
    """Stream response in real-time and save to history."""
    
    # OPTIMIZATION: Only use last 6 messages to save tokens
    # This prevents context window overload while maintaining conversation flow
    recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
    
    # Convert conversation history to LangChain message format
    messages = [
        (HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]))
        for msg in recent_history
    ]
    
    # Add current user message
    messages.append(HumanMessage(content=user_message))
    
    # Add to history
    conversation_history.append({"role": "user", "content": user_message})
    
    full_response = ""
    
    try:
        # Stream response from agent (yield tokens as they arrive)
        for chunk in agent.stream({"messages": messages}, stream_mode="messages"):
            token, _ = chunk  # Unpack token and metadata
            
            # Check if token has content attribute
            if hasattr(token, 'content') and token.content:
                full_response += token.content
                yield full_response  # Yield progressive response for UI streaming
            elif hasattr(token, 'content_blocks'):
                # Handle content_blocks format
                for block in token.content_blocks:
                    if isinstance(block, dict) and block.get('type') == 'text':
                        full_response += block.get('text', '')
                        yield full_response
    except Exception as e:
        # Handle errors gracefully
        full_response = f"❌ Error: {str(e)}"
        yield full_response
    
    # Save response to conversation history
    conversation_history.append({"role": "assistant", "content": full_response})

# ============ NON-STREAMING FALLBACK ============
def process_message(agent, user_message: str, conversation_history: list) -> tuple[str, list]:
    """Non-streaming fallback (if streaming fails)."""
    
    # Use last 6 messages for context
    recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
    
    # Convert to LangChain message format
    messages = [
        (HumanMessage(content=msg["content"]) if msg["role"] == "user" else AIMessage(content=msg["content"]))
        for msg in recent_history
    ]
    
    # Add current message
    messages.append(HumanMessage(content=user_message))
    
    try:
        # Invoke agent (non-streaming)
        result = agent.invoke({"messages": messages})
        response_content = result["messages"][-1].content if result["messages"] else "No response"
    except Exception as e:
        # Return error message if agent fails
        response_content = f"❌ Error: {str(e)}"
    
    # Update history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": response_content})
    
    return response_content, conversation_history