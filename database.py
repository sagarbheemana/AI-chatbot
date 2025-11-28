# ============ IMPORTS ============
import json  # For saving/loading JSON files
import os  # For file operations
from datetime import datetime  # For timestamps

# ============ CONFIGURATION ============
# File where all conversations will be stored
HISTORY_FILE = "conversation_history.json"

# ============ SAVE CONVERSATION ============
def save_history(conversation_history: list, user_id: str = "default"):
    """Save conversation to JSON file with timestamp and user ID."""
    
    # Create data structure for this conversation session
    data = {
        "user_id": user_id,  # Track which user this conversation belongs to
        "timestamp": datetime.now().isoformat(),  # When this conversation happened
        "messages": conversation_history  # All messages (user + AI)
    }
    
    # Read existing history from file (if it exists)
    all_history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            all_history = json.load(f)
    
    # Add this new conversation to history
    all_history.append(data)
    
    # Write everything back to file
    with open(HISTORY_FILE, "w") as f:
        json.dump(all_history, f, indent=2)

# ============ LOAD CONVERSATION ============
def load_history(user_id: str = "default") -> list:
    """Load the most recent conversation for a user."""
    
    # Return empty list if file doesn't exist (first time user)
    if not os.path.exists(HISTORY_FILE):
        return []
    
    # Read all conversations from file
    with open(HISTORY_FILE, "r") as f:
        all_history = json.load(f)
    
    # Find and return the most recent conversation for this user
    # reversed() to search from newest to oldest
    for session in reversed(all_history):
        if session.get("user_id") == user_id:
            return session.get("messages", [])
    
    # Return empty list if no conversation found for user
    return []

# ============ GET ALL CONVERSATIONS ============
def get_all_conversations():
    """Get all saved conversations from file."""
    
    # Return empty list if file doesn't exist
    if not os.path.exists(HISTORY_FILE):
        return []
    
    # Read and return all conversations
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

# ============ DELETE CONVERSATION ============
def delete_conversation(user_id: str, timestamp: str):
    """Delete a specific conversation by user_id and timestamp."""
    
    # Return early if file doesn't exist
    if not os.path.exists(HISTORY_FILE):
        return
    
    # Read all conversations
    with open(HISTORY_FILE, "r") as f:
        all_history = json.load(f)
    
    # Filter out the conversation to delete
    # Keep all conversations EXCEPT the one matching user_id and timestamp
    all_history = [s for s in all_history if not (s.get("user_id") == user_id and s.get("timestamp") == timestamp)]
    
    # Write updated history back to file
    with open(HISTORY_FILE, "w") as f:
        json.dump(all_history, f, indent=2)