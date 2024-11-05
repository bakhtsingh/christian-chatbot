import requests
import streamlit as st

# API key for Prediction Guard (make sure to store it securely in Streamlit secrets or environment variables)
PREDICTION_GUARD_API_KEY = "BcJzXHGjO3XNrpwHOTSYveOe2glUdrbrECukDtF1"

# Define model and context/system message for the assistant
MODEL = "Hermes-3-Llama-3.1-70B"
SYSTEM_PROMPT = """
You are an AI assistant knowledgeable about Christian nonprofit work, data analysis, 
and AI/ML technologies. Provide clear, helpful answers for users seeking guidance in 
these areas, and suggest resources when appropriate.
"""

with st.sidebar:
    st.title('🤖💬 Prediction Guard Chatbot')
    st.success('API key securely set up!', icon='✅')

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
if prompt := st.chat_input("What is up?"):
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
    
    # Send request to Prediction Guard API
    headers = {
        "Authorization": f"Bearer {PREDICTION_GUARD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = requests.post(
                "https://globalpath.predictionguard.com",
                headers=headers,
                json=data,
                stream=True
            )
            
            # Stream response from API
            for line in response.iter_lines():
                if line:
                    content = line.decode("utf-8")
                    # Extract content if structured data received
                    if "choices" in content:
                        full_response += content["choices"][0]["delta"].get("content", "")
                        message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
