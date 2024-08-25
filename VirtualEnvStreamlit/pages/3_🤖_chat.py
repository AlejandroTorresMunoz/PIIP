import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.llms import Ollama


# Configuration of the page 
st.set_page_config(page_title="Chat", page_icon=":robot_face:")
if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please. log in.")

# Methods executed only once
@st.cache_resource
def load_model():
    # Method only executed once at the load of the page
    st.session_state.chat_model = Ollama(model="llama3.1:8b")
    # Description provided to the model
    st.session_state.chat_description = """Eres un asistente virtual en el contexto de una página de noticias y recomendaciones de finanzas. Debes responder a las preguntas que te plantee el usuario, así como ejecutar las funciones que te solicite.""" 

# Load the LLM model
load_model()

# Create the chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Create the prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", st.session_state.chat_description), # Description provided to the model
        MessagesPlaceholder(variable_name="chat_history"), # History of the chat object
        ("human", "{input}"), # Name of the variable to store the human input
    ]
)

# Create the final chain of the LangChain model
chain = prompt_template | st.session_state.chat_model


st.title("Chat")

# User input box
user_input = st.text_input("Escribe tu consulta : ", key="user_input")
# Send button
if st.button("Enviar"):
    # Generate response
    response = chain.invoke({"input": user_input, "chat_history" : st.session_state["chat_history"]})
    # Update chat history
    st.session_state["chat_history"].append(HumanMessage(content=user_input))
    st.session_state["chat_history"].append(AIMessage(content=response))

# Chat display
chat_display = ""
for msg in st.session_state["chat_history"]:
    if isinstance(msg, HumanMessage):
        chat_display += f"Humano : {msg.content}\n"
    elif isinstance(msg, AIMessage):
        chat_display += f"Bot : {msg.content}\n"

st.text_area("Chat", value=chat_display, height=400, key="chat_area")



    