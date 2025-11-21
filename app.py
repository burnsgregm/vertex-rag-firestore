
import streamlit as st
import requests
import json

# Configuration
API_URL = "https://rag-retrieval-api-lqgrtseknq-uc.a.run.app"

# Page Setup
st.set_page_config(page_title="Enterprise RAG", layout="wide")
st.title("Test Medical Knowledge Base V2")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle User Input
if prompt := st.chat_input():
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Searching Knowledge Base..."):
        try:
            # Call Backend API
            response = requests.post(API_URL, json={"query": prompt})

            # Robust Error Handling
            if response.status_code != 200:
                st.error(f"Server Error ({response.status_code}): {response.text}")
            else:
                try:
                    data = response.json()
                    answer = data.get("answer", "Error: No answer returned")

                    # Display Answer
                    st.chat_message("assistant").write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    # Display Sources
                    with st.expander("View Sources"):
                        st.text(data.get("context_used", "No context metadata available."))

                except json.JSONDecodeError:
                    st.error(f"Invalid JSON response: {response.text}")

        except Exception as e:
            st.error(f"Connection Error: {e}")
