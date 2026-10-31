import streamlit as st
import json
import os
import random

DATABASE_FILE = "ai_memory.json"

def load_memory():
    if op.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "unknown_word" not in st.session_state:
    # Tracks if the AI is currently waiting for a definition of an unknown phrase
    st.session_state.unknown_word = None

st.title("🧠 The Blank Slate AI (Fixed)")
st.caption("Now with Interactive Training Mode!")

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
    
    # CASE A: The AI previously hit a blank wall and asked you to teach it
    if st.session_state.unknown_word:
        target_phrase = st.session_state.unknown_word
        
        if target_phrase not in st.session_state.memory:
            st.session_state.memory[target_phrase] = []
            
        if clean_input not in st.session_state.memory[target_phrase]:
            st.session_state.memory[target_phrase].append(clean_input)
            save_memory(st.session_state.memory)
            
        ai_response = f"Got it! I saved that. From now on, when you say '{target_phrase}', I might reply with '{user_input}'."
        st.session_state.unknown_word = None # Clear the training flag

    # CASE B: Standard conversational lookup
    else:
        if clean_input in st.session_state.memory and st.session_state.memory[clean_input]:
            # The AI found an answer it has learned before!
            ai_response = random.choice(st.session_state.memory[clean_input])
        else:
            # The AI hits a blank wall. It flags this word to learn it on the next turn!
            ai_response = f"I have never heard the phrase '{user_input}' before. What should I say when you say that?"
            st.session_state.unknown_word = clean_input

    # 4. Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.chat_history.append({"role": "assistant", "text": ai_response})
