from openai import OpenAI
import os
import streamlit as st
from dotenv import load_dotenv

# Set up page config early
st.set_page_config(page_title="OpenAI Chatbot", layout="wide", page_icon="🤖")

# Load environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = OpenAI(api_key=api_key, base_url=base_url)

# --- Custom CSS for ChatGPT-style UI ---
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        .chat-bubble {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.5rem;
            line-height: 1.6;
        }
        .user {
            background-color: #0059b3;
            color: white;
            text-align: right;
        }
        .assistant {
            background-color: #2f2f2f;
            color: white;
        }
        input {
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='color:white;'>🤖 OpenAI Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f"<div class='chat-bubble {role_class}'><strong>{msg['role'].capitalize()}:</strong><br>{msg['text']}</div>", unsafe_allow_html=True)

# Input and response handler
def handle_input():
    user_text = st.session_state.user_input.strip()
    if user_text:
        st.session_state.messages.append({"role": "user", "text": user_text})
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful and detailed assistant. Always explain your answers clearly and thoroughly."},
                        *[{"role": m["role"], "content": m["text"]} for m in st.session_state.messages]
                    ]
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "text": reply})
                st.session_state.user_input = ""
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Input box
st.text_input("Type your message...", key="user_input", on_change=handle_input, placeholder="Ask anything...")
