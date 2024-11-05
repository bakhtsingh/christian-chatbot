import streamlit as st
import json
from predictionguard import PredictionGuard  # Assuming Prediction Guard has a Python SDK

# Configuration (could also be moved to a config file or environment variables)
cfg = {
    "predictionguard": {
        "url": " https://globalpath.predictionguard.com",
        "api_key": "BcJzXHGjO3XNrpwHOTSYveOe2glUdrbrECukDtF1"  # Replace with your actual API key
    }
}

# Initialize the Prediction Guard client
client = PredictionGuard(
    url=cfg["predictionguard"]["url"],
    api_key=cfg["predictionguard"]["api_key"]
)

# Define model and context/system message for the assistant
MODEL = "Hermes-3-Llama-3.1-70B"
SYSTEM_PROMPT = """
You are an AI assistant knowledgeable about Christian nonprofit work, data analysis, 
and AI/ML technologies. Provide clear, helpful answers for users seeking guidance in 
these areas, and suggest resources when appropriate.
"""

# Streamlit app setup
st.title("🤖 Prediction Guard Chatbot")

# Initialize session state to store conversation messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Collect user input and handle chat completion
if prompt := st.chat_input("Ask me anything!"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare data for Prediction Guard API
    data = {
        "model": MODEL,
        "messages": st.session_state.messages,
        "max_tokens": 1000,
        "temperature": 0.5,
        "stream": True
    }
    
    # Placeholder to display streaming response from the assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Send streaming request to Prediction Guard API
            response = client.chat.completions.create(**data)

            # Stream response
            for delta in response['choices']:
                delta_content = delta.get("content", "")
                full_response += delta_content
                message_placeholder.markdown(full_response + "▌")  # Display with typing indicator
            
            # Finalize response display
            message_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
