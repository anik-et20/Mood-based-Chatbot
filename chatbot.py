import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

load_dotenv()

model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

st.set_page_config(page_title="AI Mood Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 AI Mood Chatbot")
st.caption("Choose the personality of the AI and start chatting")

# ----------- Mood Selection -----------
if "mood_selected" not in st.session_state:
    st.session_state.mood_selected = False

if not st.session_state.mood_selected:

    st.subheader("Select AI Personality")

    mood = st.radio(
        "How should the AI respond?",
        ["Funny 😂", "Angry 😡", "Sad 😢", "Happy 😊", "Calm 😌"]
    )

    if st.button("Start Chatting"):
        if mood == "Funny 😂":
            role = "You are a funny Ai agent"
        elif mood == "Angry 😡":
            role = "You are an angry Ai agent that replies angrily"
        elif mood == "Sad 😡":
            role = "You are a sad Ai agent that replies sadly"
        elif mood == "Angry 😡":
            role = "You are an angry Ai agent that replies happily"
        else:
            role = "You are a sad Ai agent that replies calmy"

        st.session_state.messages = [SystemMessage(content=role)]
        st.session_state.mood_selected = True
        st.rerun()

# ----------- Chat UI -----------
if st.session_state.mood_selected:

    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)

        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

    # Chat input
    prompt = st.chat_input("Type your message... (0 to exit)")

    if prompt:

        if prompt == "0":
            st.stop()

        with st.chat_message("user"):
            st.write(prompt)

        st.session_state.messages.append(HumanMessage(content=prompt))

        response = model.invoke(st.session_state.messages)

        st.session_state.messages.append(AIMessage(content=response.content))

        with st.chat_message("assistant"):
            st.write(response.content)