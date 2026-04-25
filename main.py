import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Babar's AI Chatbot", page_icon="🤖")

st.title("🤖 Babar's AI Helper")
st.markdown("Welcome! Main aapka AI assistant hoon. Poochye jo poochna hai.")

# API Key setup (Streamlit Secrets se uthayega)
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("API Key nahi mili. Please Streamlit settings mein 'Secrets' check karen.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Yahan sawal likhen..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Get response from Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False,
        )
        
        full_response = response.choices[0].message.content
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Error: {e}")
