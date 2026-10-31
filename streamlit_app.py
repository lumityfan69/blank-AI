import streamlit as st
import random

# --- CHAT BRAIN INITIALIZATION ---
# We store the memory inside st.session_state so it is private to this browser tab.
# We no longer read or write to a shared JSON file.
if "isolated_memory" not in st.session_state:
    st.session_state.isolated_memory = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "unknown_word" not in st.session_state:
    st.session_state.unknown_word = None

# --- PRIVATE SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Private Brain Settings")
    st.write("Phrases learned in this session:", len(st.session_state.isolated_memory))
    st.info("Your AI's memory is private to this browser tab. Refreshing or closing the tab resets it back to zero!")
    
    # Red button to erase ONLY this user's memory state
    if st.button("🚨 Reset My AI Memory", type="primary"):
        st.session_state.isolated_memory = {}
        st.session_state.chat_history = []
        st.session_state.unknown_word = None
        st.success("Your private session has been wiped clean!")
        st.rerun()

# --- MAIN CHAT INTERFACE ---
st.title("🧠 The Isolated Blank Slate AI")
st.caption("Your own private version of the AI. It learns exclusively from your text inputs during this session!")

# Display full chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Handle user input
if user_input := st.chat_input("Type something to teach your AI..."):
    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    clean_input = user_input.strip().lower()
    
    # CASE A: The AI is waiting for a definition of an unknown phrase
    if st.session_state.unknown_word:
        target_phrase = st.session_state.unknown_word
        
        if target_phrase not in st.session_state.isolated_memory:
            st.session_state.isolated_memory[target_phrase] = []
            
        if clean_input not in st.session_state.isolated_memory[target_phrase]:
            st.session_state.isolated_memory[target_phrase].append(clean_input)
            
        ai_response = f"Got it! I saved that. From now on, when you say '{target_phrase}', I might reply with '{user_input}'."
        st.session_state.unknown_word = None 

    # CASE B: Standard conversational lookup
    else:
        if clean_input in st.session_state.isolated_memory and st.session_state.isolated_memory[clean_input]:
            ai_response = random.choice(st.session_state.isolated_memory[clean_input])
        else:
            ai_response = f"I have never heard the phrase '{user_input}' before. What should I say when you say that?"
            st.session_state.unknown_word = clean_input

    # 4. Display AI response
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.chat_history.append({"role": "assistant", "text": ai_response})
