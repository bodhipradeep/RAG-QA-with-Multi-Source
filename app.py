import os
import streamlit as st
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.tools import Tool
from tools import get_tools, llm
import os

# Sidebar for file uploads (CSV, Text, PDF)
with st.sidebar:
    st.title("API & File Uploader")
    api_key = st.sidebar.text_input("Please provide Groq API Key", type="password")
    csv = st.sidebar.file_uploader("Upload CSV file only", type="csv") or None
    text = st.sidebar.file_uploader("Upload Text file only", type="txt") or None
    pdf = st.sidebar.file_uploader("Upload PDF file only", type="pdf") or None
    
# Main chat interface for Q&A
st.title("RAG-Based Q&A Chatbot")

# Validating GROQ API
if not api_key:
    st.warning("Please provide a valid GROQ API Key to continue.")
    st.stop()
os.environ["GROQ_API_KEY"] = api_key

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("You are a helpful assistant. Always use tools to answer the user's question."),
    HumanMessagePromptTemplate.from_template("{input}"),
    MessagesPlaceholder(variable_name='agent_scratchpad')
])

# Handles user input through chat
if user_input := st.chat_input("Ask any Query"):
    # Shows processing status with spinner
    with st.spinner("Analyzing ..."):
        try:            
            # assign file for tools
            tools = get_tools(csv=csv, text=text, pdf=pdf)

            # Agent Initialization:
            def agent(query):
                agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
                agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
                response = agent_executor.invoke({"input": query})
                return response['output']

            result = agent(user_input)
        except Exception as e:
            result = f"An error occurred: {str(e)}"

        # Display Result if any
        if result:
            # Displays conversation with avatars        
            with st.chat_message("user", avatar="🧔‍♂️"):
                st.markdown(user_input)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(result)

