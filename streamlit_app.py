import streamlit as st
import random

# --- INITIALIZATION ---
if "isolated_memory" not in st.session_state:
    st.session_state.isolated_memory = {}  # Conversational responses

if "dictionary" not in st.session_state:
    st.session_state.dictionary = {}       # Core definitions/meanings

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "learning_state" not in st.session_state:
    # Tracks the word and target type we are currently teaching the AI
    st.session_state.learning_state = None

# --- SIDEBAR: MODE SELECTION & CONTROLS ---
with st.sidebar:
    st.header("⚙️ Brain Control Panel")
    
    # Let the user choose how they want to interact with the AI
    app_mode = st.radio(
        "Select Interaction Mode:",
        ["Chitchat Mode 💬", "Teach Definitions 📖"]
    )
    
    st.divider()
    st.write(f"🧠 Vocabulary Learned: {len(st.session_state.dictionary)} words")
    st.write(f"💬 Conversational Links: {len(st.session_state.isolated_memory)} phrases")
    
    if st.button("🚨 Reset AI Brain", type="primary"):
        st.session_state.isolated_memory = {}
        st.session_state.dictionary = {}
        st.session_state.chat_history = []
        st.session_state.learning_state = None
        st.success("Wiped back to absolute zero!")
        st.rerun()

# --- MAIN INTERFACE ---
st.title("🧠 The Blank Slate AI")
st.caption("Now with dedicated conversational training and factual dictionary lookup!")

# Show history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# Handle interaction loop
if user_input := st.chat_input("Type here..."):
    # Display user input
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    
    clean_input = user_input.strip().lower()
    ai_response = ""

    # CASE 1: The AI is currently waiting for a piece of information from the previous turn
    if st.session_state.learning_state:
        state_type = st.session_state.learning_state["type"]
        target_word = st.session_state.learning_state["word"]
        
        if state_type == "definition":
            # Save the literal meaning of the word
            st.session_state.dictionary[target_word] = user_input.strip()
            ai_response = f"Got it! I now know that **{target_word}** means: '{user_input}'."
        
        elif state_type == "reply":
            # Save a conversation chain link
            if target_word not in st.session_state.isolated_memory:
                st.session_state.isolated_memory[target_word] = []
            if clean_input not in st.session_state.isolated_memory[target_word]:
                st.session_state.isolated_memory[target_word].append(clean_input)
            ai_response = f"Understood! If you say '{target_word}', I might reply with '{user_input}'."
            
        st.session_state.learning_state = None  # Clear training track

    # CASE 2: Mode handling for normal interaction
    else:
        # Mode A: User wants to manually program a hard word definition
        if app_mode == "Teach Definitions 📖":
            ai_response = f"I've flagged the phrase '{user_input}'. Now, please tell me: what is the **definition** of '{user_input}'?"
            st.session_state.learning_state = {"type": "definition", "word": clean_input}
            
        # Mode B: Standard Chitchat Mode
        else:
            # First, check if the user is asking for a definition (e.g., "what is apple?")
            is_asking_definition = False
            lookup_word = clean_input
            
            for trigger in ["what is ", "what's a ", "what's an ", "define "]:
                if clean_input.startswith(trigger):
                    lookup_word = clean_input.replace(trigger, "").strip()
                    is_asking_definition = True
                    break
            
            if is_asking_definition:
                if lookup_word in st.session_state.dictionary:
                    ai_response = f"According to my dictionary, **{lookup_word}** means: {st.session_state.dictionary[lookup_word]}"
                else:
                    ai_response = f"I don't know the definition of '{lookup_word}' yet. Switch my sidebar mode to 'Teach Definitions' to teach it to me!"
            else:
                # Fall back to traditional conversational dialogue response
                if clean_input in st.session_state.isolated_memory and st.session_state.isolated_memory[clean_input]:
                    ai_response = random.choice(st.session_state.isolated_memory[clean_input])
                else:
                    ai_response = f"I don't know how to chat back to '{user_input}' yet. What should I reply when you say that?"
                    st.session_state.learning_state = {"type": "reply", "word": clean_input}

    # Display and log the final AI output
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.chat_history.append({"role": "assistant", "text": ai_response})
