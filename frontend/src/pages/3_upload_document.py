import streamlit as st
import requests
from settings import BACKEND_API_URI    # type: ignore


UPLOAD_TXT_ENDPOINT = f"{BACKEND_API_URI.rstrip('/')}/rag/vectorize/upload-text"

st.set_page_config(page_title="RAG File Uploader", layout="centered")
st.title("📄 RAG Vectorize Uploader")
st.markdown(f"Upload documents to API for vectorizing them. (`.txt`, ...)")
st.markdown(f"**Target URL:** `{UPLOAD_TXT_ENDPOINT}`")

st.divider()

with st.form(key="upload_form"):
    
    uploaded_file = st.file_uploader(
        "Select your txt files to vectorize.",
        type=["txt"],
        accept_multiple_files=False 
    )
    submit_button = st.form_submit_button(label="Upload and Execute")

if submit_button:
    if uploaded_file is not None:
        files_payload = {
            'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
        }
        
        st.info(f"Uploading '{uploaded_file.name}' to server...")
        
        try:
            response = requests.post(UPLOAD_TXT_ENDPOINT, files=files_payload)
            if response.ok:
                st.success("Uploaded successfully.")
                st.json(response.json())
            else:
                st.error(f"Failed: {response.status_code}")
                st.text(f"Response:\n{response.text}")
        
        except requests.exceptions.ConnectionError:
            st.error(f"Connection error: is alive API?")
        except Exception as e:
            st.error(f"Unexepceted error: {e}")
            
    else:
        st.warning("Select your file first.")
    