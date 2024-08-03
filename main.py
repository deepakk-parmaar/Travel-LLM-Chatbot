import asyncio
import random
import streamlit as st
from chat import flight_query, hotel_query, get_route
from streamlit_folium import st_folium

if "llama_model" not in st.session_state:
    st.session_state["llama_model"] = "llama3"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "map" in message:
            st_folium(message["map"], width=700, height=500, key=f"map_{idx}")

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        route = get_route(prompt)
        if route == "flight":
            response = asyncio.run(flight_query(prompt, message_placeholder))
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
        elif route == "hotel":
            response, hotel_map = asyncio.run(
                hotel_query(prompt, message_placeholder))
            st.session_state.messages.append(
                {"role": "assistant", "content": response, "map": hotel_map})
            st_folium(hotel_map, width=700, height=500,
                      key=random.randint(0, 1000))

        else:
            response = "I am not sure what you are asking for. Please ask again"
            st.session_state.messages.append(
                {"role": "assistant", "content": response})
        message_placeholder.markdown(response)

# # Display stored hotel map if available
# for idx, message in enumerate(st.session_state.messages):
#     if message["role"] == "assistant" and "map" in message:
