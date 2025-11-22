import os
import streamlit as st
from google import genai
from google.genai import types

# IMPORTANT: Using python_gemini blueprint for Gemini integration
# API key is from Gemini Developer API Key, not Vertex AI
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini Chatbot")
st.caption("Powered by Google Gemini AI")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Prepare chat history for context
            contents = []
            for msg in st.session_state.messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
            
            # Stream response from Gemini
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents
            )
            
            # Display streaming response
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            # Final response without cursor
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.error(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar with controls
with st.sidebar:
    st.header("Chat Controls")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.subheader("About")
    st.info(
        "This chatbot uses Google's Gemini AI model to provide "
        "intelligent responses. Your conversation history is maintained "
        "within this session."
    )
    
    st.divider()
    
    st.caption(f"Messages: {len(st.session_state.messages)}")
