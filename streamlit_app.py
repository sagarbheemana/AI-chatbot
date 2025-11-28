# streamlit_app.py
# Streamlit UI for the AI chatbot with persistent conversation history

import streamlit as st  # Web UI
import time  # timing responses
from datetime import datetime  # format timestamps

# AI logic and persistence helpers (must exist in your project)
from tool_router import create_chatbot_agent, process_message_streaming
from database import save_history, load_history, get_all_conversations, delete_conversation

# -------------------------
# Page configuration
# -------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 AI Assistant with Memory")
st.markdown("**Chat now**")

# -------------------------
# Session state initialization
# -------------------------
if "agent" not in st.session_state:
    # Create single agent instance and reuse it
    st.session_state.agent = create_chatbot_agent()

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "user_id" not in st.session_state:
    st.session_state.user_id = "225523"

if "show_past" not in st.session_state:
    st.session_state.show_past = False

# -------------------------
# Sidebar: conversation manager
# -------------------------
with st.sidebar:
    st.header("💬 Conversation Manager")

    # User identifier (used to save/load user-specific histories)
    user_id = st.text_input("Your ID:", value=st.session_state.user_id)
    st.session_state.user_id = user_id

    st.divider()

    # Toggle viewing past conversations
    if st.button("📂 View Past Conversations", use_container_width=True):
        st.session_state.show_past = not st.session_state.show_past

    # Show list of past conversations (if toggled)
    if st.session_state.show_past:
        st.subheader("📜 Past Chats")
        all_convs = get_all_conversations()  # returns list of saved sessions

        if all_convs:
            # Display in reverse order (newest first)
            for i, conv in enumerate(reversed(all_convs)):
                timestamp = conv.get("timestamp", "Unknown")
                try:
                    dt = datetime.fromisoformat(timestamp)
                    display_time = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    display_time = timestamp

                # preview of first message
                first_message = conv.get("messages", [{}])[0].get("content", "Empty")[:50]

                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(f"📌 {display_time}\n{first_message}...", key=f"conv_{i}", use_container_width=True):
                        # Load this conversation into current session
                        st.session_state.conversation_history = conv.get("messages", [])
                        st.session_state.show_past = False
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{i}"):
                        # Delete specific conversation (uses timestamp & user_id)
                        delete_conversation(user_id, timestamp)
                        st.experimental_rerun()
        else:
            st.info("No past conversations yet. Start chatting!")

    st.divider()
    st.subheader("⚙️ Chat Controls")

    col1, col2 = st.columns(2)
    with col1:
        # Clear current in-memory conversation
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.conversation_history = []
            st.experimental_rerun()
    with col2:
        # Save current conversation to persistent store (JSON file)
        if st.button("💾 Save", use_container_width=True):
            if st.session_state.conversation_history:
                save_history(st.session_state.conversation_history, st.session_state.user_id)
                st.success("Conversation saved.")
            else:
                st.warning("Nothing to save yet.")

    st.divider()
    st.caption("Autosave occurs after each message. Saved files kept locally.")

# -------------------------
# Display current conversation
# -------------------------
st.subheader("💬 Chat")
if st.session_state.conversation_history:
    for msg in st.session_state.conversation_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
# else:
#     st.info("👋 Start a new conversation! Ask your first question below...")

# -------------------------
# User input and streaming response
# -------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # show user message immediately
    with st.chat_message("user"):
        st.write(user_input)

    # stream assistant response
    start = time.time()
    with st.chat_message("assistant"):
        placeholder = st.empty()
        # process_message_streaming yields progressive text chunks
        for chunk in process_message_streaming(
            st.session_state.agent,
            user_input,
            st.session_state.conversation_history
        ):
            placeholder.markdown(chunk)

    # auto-save after each exchange
    save_history(st.session_state.conversation_history, st.session_state.user_id)

    elapsed = time.time() - start
    st.caption(f"⚡ {elapsed:.1f}s | 💾 Saved")

st.divider()
st.caption(f"📊 {len(st.session_state.conversation_history)} messages | 🟢 Ollama local")