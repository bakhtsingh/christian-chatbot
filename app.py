import requests
import streamlit as st
import json

# Prediction Guard API configuration
API_URL = "https://api.predictionguard.com/chat/completions"
API_KEY = "BcJzXHGjO3XNrpwHOTSYveOe2glUdrbrECukDtF1"  # Replace with your actual API key

# Define model and context/system message for the assistant
MODEL = "Hermes-3-Llama-3.1-70B"  # Use the 70B model
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
        "temperature": 1,
        "top_p": 1,
        "top_k": 50,
        "stream": True,
        "input": {
            "pii": "replace",
            "pii_replace_method": "random"
        }
    }
    
    # Placeholder to display streaming response from the assistant
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Send streaming request to Prediction Guard API
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            response = requests.post(API_URL, headers=headers, json=data, stream=True)

            # Stream response by iterating over each line of streamed data
            for line in response.iter_lines():
                if line:
                    # Parse JSON response and retrieve content
                    content_data = json.loads(line.decode("utf-8"))
                    delta_content = content_data["data"]["choices"][0]["delta"].get("content", "")
                    full_response += delta_content
                    message_placeholder.markdown(full_response + "▌")  # Display with typing indicator
            
            # Finalize response display
            message_placeholder.markdown(full_response)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
