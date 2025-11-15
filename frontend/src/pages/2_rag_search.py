import streamlit as st
import requests
from settings import BACKEND_API_URI    # type: ignore

RAG_ENDPOINT = f"{BACKEND_API_URI.rstrip('/')}/rag/chat"

st.set_page_config(page_title="RAG Demo", layout="centered")

st.title("RAG Demo - General Conversation")

if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# if sector != "All":
#     payload["sector"] = sector

if prompt := st.chat_input("Your question:"):
    st.session_state.rag_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {"question": prompt}
    with st.chat_message("assistant"):
        stream = 'No result.'
        try:
            response = requests.post(RAG_ENDPOINT, json=payload)
            data = response.json()
            if "message" in data and data["message"]:
                stream = data['message']
        except Exception as e:
            st.error(f"Error fetching data: {e}")
        response = st.write(stream)
    st.session_state.rag_messages.append({"role": "assistant", "content": response})
