from openai import OpenAI
import streamlit as st

# --- Setup page ---
st.set_page_config(page_title="OpenAI Chatbot", layout="wide", page_icon="🤖")

# --- Load secrets from Streamlit ---
api_key = st.secrets.get("OPENAI_API_KEY", "")
base_url = st.secrets.get("OPENAI_BASE_URL", "")

if not api_key:
    st.error("❌ OPENAI_API_KEY not found in Streamlit secrets. Please add it in Settings → Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url=base_url)

# --- Custom ChatGPT-style UI ---
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: white;
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

st.markdown("<h1 style='color:white;'>🤖 OpenAI Chatbot</h1>", unsafe_allow_html=True)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f"<div class='chat-bubble {role_class}'><strong>{msg['role'].capitalize()}:</strong><br>{msg['text']}</div>",
        unsafe_allow_html=True
    )

# --- Handle user input ---
def handle_input():
    user_text = st.session_state.user_input.strip()
    if not user_text:
        return

    st.session_state.messages.append({"role": "user", "text": user_text})
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful and detailed assistant."},
                    *[{"role": m["role"], "content": m["text"]} for m in st.session_state.messages]
                ]
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "text": reply})
        except Exception as e:
            st.error(f"❌ Error: {e}")
    st.session_state.user_input = ""

# --- Input text box ---
st.text_input("Type your message...", key="user_input", on_change=handle_input, placeholder="Ask anything...")
