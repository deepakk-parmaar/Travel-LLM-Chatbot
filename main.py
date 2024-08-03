import asyncio
import streamlit as st
from chat import flight_query

if "llama_model" not in st.session_state:
    st.session_state["llama_model"] = "llama3"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = asyncio.run(flight_query(prompt, message_placeholder))
        message_placeholder.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
