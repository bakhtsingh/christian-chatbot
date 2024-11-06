import os
import streamlit as st
from predictionguard import PredictionGuard

# Set up your Prediction Guard API client
client = PredictionGuard(
    url="https://globalpath.predictionguard.com",
    api_key="BcJzXHGjO3XNrpwHOTSYveOe2glUdrbrECukDtF1"
)

# Load the system prompt from a separate file
with open("system_prompt.txt", "r") as file:
    system_prompt_content = file.read()

# Define the system prompt for theological perspective (won't appear in the UI)
system_prompt = {
    "role": "system",
    "content": system_prompt_content
}

# Sidebar with Chatbot info
with st.sidebar:
    st.title("📖🙏 Christian Q&A Chatbot")
    st.write("Ask questions about Christianity, theology, and the Bible.")

# Initialize the conversation session state
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# Display all previous messages in the chat history, excluding the system prompt
for message in st.session_state.messages:
    if message["role"] != "system":  # Skip displaying the system prompt
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input prompt at the bottom for the user to ask a question
if user_input := st.chat_input("Enter your question here..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare assistant's response container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Stream assistant response from Prediction Guard
        for res in client.chat.completions.create(
            model="Hermes-3-Llama-3.1-70B",
            messages=st.session_state.messages,
            max_tokens=13500,
            temperature=0.1,
            stream=True
        ):
            # Append each piece of content to full_response and update display
            full_response += res["data"]["choices"][0]["delta"].get("content", "")
            message_placeholder.markdown(full_response + "▌")

        # Finalize the assistant response without cursor
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
