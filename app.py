import os
import streamlit as st
from predictionguard import PredictionGuard

# Set up your Prediction Guard API key
client = PredictionGuard(url="https://globalpath.predictionguard.com",
    api_key="BcJzXHGjO3XNrpwHOTSYveOe2glUdrbrECukDtF1"
)

# Define the system prompt based on your theological perspective and instructions
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

# Initialize the Streamlit app
st.title("Christian Q&A Chatbot")
st.write("Ask a question related to Christianity, and receive answers from a conservative evangelical perspective.")

# Get user input
user_question = st.text_input("Enter your question:")

if st.button("Ask"):
    if user_question:
        # Initialize the chat messages with the system prompt and the user question
        messages = [
            system_prompt,
            {
                "role": "user",
                "content": user_question
            }
        ]
        
        # Create an empty container for displaying the streaming response
        response_container = st.empty()
        
        # Collect response from Prediction Guard API in a streaming format
        response_text = ""
        for res in client.chat.completions.create(
            model="Hermes-2-Pro-Llama-3-8B",
            messages=messages,
            max_tokens=500,
            temperature=0.1,
            stream=True
        ):
            # Append the new content to the response text
            response_text += res["data"]["choices"][0]["delta"]["content"]
            
            # Update the container with the latest response text to simulate streaming
            response_container.write(response_text)
    else:
        st.warning("Please enter a question before pressing 'Ask'.")
