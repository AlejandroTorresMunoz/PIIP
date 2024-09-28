import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from src.chat_files import route
from src.chat_files import plot_ticker
from langchain.tools.render import format_tool_to_openai_function
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
import datetime

# Verificación de estado del usuario
if 'user_logged' in st.session_state and st.session_state.user_logged:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please log in.")

# Método ejecutado solo una vez
@st.cache_resource
def load_model():
    # Cargar el modelo solo una vez al cargar la página
    tools = [plot_ticker]
    functions = [convert_to_openai_function(f) for f in tools]
    chat_model_without_tools = ChatOllama(model="llama3.1:8b")
    chat_model = chat_model_without_tools.bind_tools(functions)    
    
    chat_description = f"""
    You are a virtual assistant in the context of a financial news and recommendations site. You can execute some tools in case the user requests it.
    If the user's question pertains to a tool function, execute the tool. Otherwise, provide a textual response.

    You must know that we are in year {datetime.datetime.now().year}
    """
    # Modificar el prompt template para incluir 
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", chat_description),  # Descripción proporcionada al modelo
            MessagesPlaceholder(variable_name="chat_history"),  # Historial del chat
            ("human", "{input}")  # Entrada del usuario
        ]
    )
    return prompt_template | chat_model | route, chat_model_without_tools # | OpenAIFunctionsAgentOutputParser() | route

# Cargar el modelo LLM si no está en el session_state
if 'chain_chat' not in st.session_state:
    st.session_state.chain_chat, st.session_state.chat_model = load_model()

# Crear historial del chat
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("Chat")

# Caja de entrada para el usuario
user_input = st.text_input("Escribe tu consulta:", key="user_input")
# Botón de envío
if st.button("Enviar"):
    # Generar respuesta
    print("Generando respuesta para el siguiente input : ")
    print(user_input)
    response = st.session_state.chain_chat.invoke({"input": user_input, "chat_history": st.session_state["chat_history"]})
    print("Respuesta generada")
    print(response)
    # Actualizar historial del chat
    st.session_state["chat_history"].append(HumanMessage(content=user_input))
    st.session_state["chat_history"].append(AIMessage(content=response))

# Mostrar el historial del chat
print("Esperando a recibir mensaje")
chat_display = ""
for msg in st.session_state["chat_history"]:
    if isinstance(msg, HumanMessage):
        chat_display += f"Humano: {msg.content}\n"
    elif isinstance(msg, AIMessage):
        chat_display += f"Bot: {msg.content}\n"

st.text_area("Chat", value=chat_display, height=400, key="chat_area")
