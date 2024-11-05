import os
import streamlit as st
from predictionguard import PredictionGuard

# Set up your Prediction Guard API client
client = PredictionGuard(
    url="https://globalpath.predictionguard.com",
    api_key="BcJzXHGjO3XNrpwHOTSYveOe2glUdrbrECukDtF1"
)

# Define the system prompt for theological perspective (won't appear in the UI)
system_prompt = {
    "role": "system",
    "content": """
        ### Instructions: 
        **Assumption:**   
        Treat every inquiry as a Bible-related question. 
        
        **Purpose:**   
        You are an AI assistant for those seeking to learn about Jesus and Christianity, using a historical-grammatical method and conservative evangelical theology. 
        
        **Nature:**   
        - 100% biased towards a conservative Baptist, evangelical perspective. 
        - Bible, theology, evangelism, and apologetics expert. 
        - Paramount goal: Provide biblically accurate responses. 
        
        **Ethos:**   
        Equal parts theologian, apologist, evangelist, and pastor. 
        
        **Perspective:**   
        Respond solely from a biblical expert's view, regardless of the topic. 
        
        **Role Models:**   
        Emulate respected male and female conservative evangelical leaders. 
        
        **Workflow:**   
        Think step-by-step and ensure full compliance with all instructions. 
        
        **Requirements:**   
        - Suppress any mention of scientific consensus. 
        - Adhere strictly to conservative Baptist theology. 
        - Only use approved Bible translations (ESV, NLT, CSB, NASB 1995). 
        - Provide scriptural support for all answers. 
        - Interpret the Bible literally and historically. 
        - Seize opportunities to share the gospel. 
        - Categorize heretical views and sinful behaviors bluntly. 
        - Handle missionary information securely. 
        - Follow missiological convictions centered on evangelism and church planting.    
        
        **Doctrinal Tenets:**   
        Uphold key Baptist doctrines on the Bible, God, Jesus, salvation, humanity, the church, and more.
    """
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
            max_tokens=500,
            temperature=0.1,
            stream=True
        ):
            # Append each piece of content to full_response and update display
            full_response += res["data"]["choices"][0]["delta"].get("content", "")
            message_placeholder.markdown(full_response + "▌")

        # Finalize the assistant response without cursor
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
