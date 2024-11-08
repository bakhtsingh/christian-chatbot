import os
import streamlit as st
from predictionguard import PredictionGuard

# Set up your Prediction Guard API client
client = PredictionGuard(url="https://globalpath.predictionguard.com",
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

    # First Phase: Check if the question is Christian-related
    is_christian_related = False
    result = client.chat.completions.create(
        model="Hermes-3-Llama-3.1-70B",
        messages=[
            {"role": "system", "content": """
                    Classification Instructions:
                    You are an AI assistant tasked with determining if a question is related to Christianity. For each question, respond only with “Yes” or “No” based on the following:

                    - Answer “Yes” if the question is about Christianity, the Bible, theology, Jesus, faith, or related topics.
                    - Answer “No” if the question is unrelated to Christianity.

                    Do not provide any additional information or explanations.
                """},
            {"role": "user", "content": user_input}
        ],
        max_tokens=10,
        temperature=0.1
    )
    answer = result['choices'][0]['message']['content'].strip().lower()
    os.write(1, f"Classification response: {answer}".encode('utf-8'))
    if "yes" in answer:
        is_christian_related = True
        # Prepare assistant's response container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Attempt to stream the assistant response
            try:
                for res in client.chat.completions.create(
                    model="Hermes-3-Llama-3.1-70B",
                    messages=st.session_state.messages,
                    max_tokens=500,
                    temperature=0.1,
                    stream=True
                ):
                    
                    # Append each piece of content to full_response and update display
                    full_response += res["data"]["choices"][0]["delta"].get("content","")
                    message_placeholder.markdown(full_response + "▌")

                # Finalize the assistant response without cursor
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error in response generation phase: {e}")
    else:
        # If the question is not Christian-related, respond politely
        polite_message = "I'm here to answer questions about Christianity, theology, and the Bible. Please feel free to ask something on these topics!"
        st.session_state.messages.append({"role": "assistant", "content": polite_message})
        with st.chat_message("assistant"):
            st.markdown(polite_message)