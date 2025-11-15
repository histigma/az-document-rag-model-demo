import streamlit as st
import requests
from settings import BACKEND_API_URI        # type: ignore

CHAT_ENDPOINT = f"{BACKEND_API_URI.rstrip('/')}/chat/test"


st.set_page_config(page_title="Test Conversation", layout="centered")

st.title("Test Conversation with OpenAI (Pure)")


# query = st.text_input("Conversation Start: ")
# sector = st.selectbox("Filter by sector:", ["All", "Technology", "Finance", "Healthcare"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# if sector != "All":
#     payload["sector"] = sector

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {"question": prompt}
    with st.chat_message("assistant"):
        stream = 'No result.'
        try:
            response = requests.post(CHAT_ENDPOINT, json=payload)
            data = response.json()
            if "message" in data and data["message"]:
                stream = data['message']
        except Exception as e:
            st.error(f"Error fetching data: {e}")
        response = st.write(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
