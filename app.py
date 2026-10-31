import streamlit as st
import json
import os
import random

# File to store the AI's learned memory
DATABASE_FILE = "ai_memory.json"

def load_memory():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

# Initialize memory and conversation state
if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_ai_prompt" not in st.session_state:
    # Tracks what the AI last said, so it knows what the user is replying to
    st.session_state.last_ai_prompt = None

st.title("🧠 The Blank Slate AI")
st.caption("This AI started with absolutely zero knowledge. It learns word associations entirely from you!")

# Display full chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Handle user input
if user_input := st.chat_input("Type something to teach the AI..."):
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    clean_input = user_input.strip().lower()
    
    # 2. LEARNING STEP: If the AI spoke previously, link its last utterance to this new user reply
    if st.session_state.last_ai_prompt:
        last_prompt = st.session_state.last_ai_prompt
        if last_prompt not in st.session_state.memory:
            st.session_state.memory[last_prompt] = []
        # Save the association if it doesn't already exist to avoid duplicates
        if clean_input not in st.session_state.memory[last_prompt]:
            st.session_state.memory[last_prompt].append(clean_input)
            save_memory(st.session_state.memory)

    # 3. RESPONSE STEP: Look up if AI has learned a response for the user's current input
    if clean_input in st.session_state.memory and st.session_state.memory[clean_input]:
        # Pick a random learned response tied to this phrase
        ai_response = random.choice(st.session_state.memory[clean_input])
    else:
        # Absolutely nothing known yet for this phrase! Fallback warning
        ai_response = f"...? (I don't know what '{user_input}' means yet. Reply to teach me!)"

    # 4. Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.chat_history.append({"role": "assistant", "text": ai_response})
    
    # Update tracking state for the next turn
    st.session_state.last_ai_prompt = ai_response.strip().lower()
