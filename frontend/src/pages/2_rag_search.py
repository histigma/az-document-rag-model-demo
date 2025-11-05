import streamlit as st
import requests

st.set_page_config(page_title="RAG Demo", layout="wide")

st.title("RAG Demo - General Conversation")

query = st.text_input("Conversation Start: ")
# sector = st.selectbox("Filter by sector:", ["All", "Technology", "Finance", "Healthcare"])

if st.button("Question"):
    payload = {"question": query}
    # if sector != "All":
    #     payload["sector"] = sector

    try:
        response = requests.post("http://localhost:8000/rag/chat", json=payload)
        data = response.json()
        
        st.subheader("Results:")
        if "message" in data and data["message"]:
            if isinstance(data['message'], list):
                for idx, doc in enumerate(data["results"], 1):
                    st.markdown(f"**{idx}. {doc.get('title', 'No Title')}**")
                    st.write(doc.get("content", "No content"))
                    st.caption(f"Date: {doc.get('date', 'N/A')} | Ticker: {doc.get('ticker', 'N/A')}")
            else:
                st.write(f"{data['message']}")
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
