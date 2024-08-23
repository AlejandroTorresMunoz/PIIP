import streamlit as st


# Configuration of the page 
st.set_page_config(page_title="Chat", page_icon=":robot_face:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")

st.title("Chat")
# Create a memory of messages in the chats
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages form history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Accept user input
if prompt := st.chat_input("Introduce a message."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add message to chat history
    st.session_state.messages.append({'role' : 'user', 'content':prompt})




    