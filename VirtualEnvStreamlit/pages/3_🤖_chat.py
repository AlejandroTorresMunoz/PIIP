import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain.agents import Tool
from langchain_core.tools import tool
from src.chat_files import plot_ticker


if 'user_logged' in st.session_state and st.session_state.user_logged == True:
    st.sidebar.write(f"User : {st.session_state.email}")
else:
    st.sidebar.write("Please log in.")

# Método ejecutado solo una vez
@st.cache_resource
def load_model():
    # Cargar el modelo solo una vez al cargar la página
    chat_model = ChatOllama(model="llama3.1:8b")
    # Cargar las funciones del modelo
    tools = [
        Tool(
            name="plot_ticker",
            func=plot_ticker,  # Aquí usamos la función decorada
            description="Plotea los valores de un ticker especificado."
        )
    ]
    
    chat_model = chat_model.bind_tools(tools)

    # Descripción proporcionada al modelo
    chat_description = """
    Eres un asistente virtual en el contexto de una página de noticias y recomendaciones de finanzas.
    Debes responder a las preguntas que te plantee el usuario, así como ejecutar las funciones que te solicite, en caso de que te sea posible.
    En caso contrario, debes responder en caso de que 
    """

    # Plantilla del prompt
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", chat_description),  # Descripción proporcionada al modelo
            MessagesPlaceholder(variable_name="chat_history"),  # Historial del chat
            ("human", "{input}"),  # Variable para almacenar la entrada del usuario
        ]
    )

    return prompt_template | chat_model

# Cargar el modelo LLM si no está en el session_state
if 'chain_chat' not in st.session_state:
    st.session_state.chain_chat = load_model()

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
