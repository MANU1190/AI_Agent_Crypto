import streamlit as st
import os
from dotenv import load_dotenv
from agent import react_agent, system_prompt  # Import your agent functions

load_dotenv()

st.title("Cryptocurrency AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system": #dont show system prompt.
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask me about cryptocurrency prices..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Call react_agent directly
        agent_response = react_agent(prompt)
        st.session_state.messages.append({"role": "assistant", "content": agent_response["response"]})
        with st.chat_message("assistant"):
            st.markdown(agent_response["response"])

    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})