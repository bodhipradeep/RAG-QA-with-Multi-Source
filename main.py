import streamlit as st
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_groq import ChatGroq
from retriever import retriever
import os

# Sidebar for file uploads (CSV, Text, PDF)
with st.sidebar:
    st.title("API & File Uploader")
    api_key = st.sidebar.text_input("Please provide Groq API Key", type="password")
    # csv = st.sidebar.file_uploader("Upload CSV file only", type="csv") or None
    text = st.sidebar.file_uploader("Upload Text file only", type="txt") or None
    pdf = st.sidebar.file_uploader("Upload PDF file only", type="pdf") or None
    
# Main chat interface for Q&A
st.title("RAG-Based Q&A Chatbot")

# Validating GROQ API
if not api_key:
    st.warning("Please provide a valid GROQ API Key to continue.")
    st.stop()
os.environ["GROQ_API_KEY"] = api_key

llm = ChatGroq(model="llama3-8b-8192", temperature=0.5, verbose=True)
# llm = ChatOllama(model="llama3.1", temperature=0, verbose=True)

prompt=ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

# Handles user input through chat
if user_input := st.chat_input("Ask any Query"):
    # Shows processing status with spinner
    with st.spinner("Analyzing ..."):
        try:            
            # assign file for tools
            retriever = retriever(text=text, pdf=pdf)

            document_chain = create_stuff_documents_chain(llm, prompt)
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            result = retrieval_chain.invoke({"input":user_input})
        except Exception as e:
            result = f"An error occurred: {str(e)}"

        # Display Result if any
        if result:
            # Displays conversation with avatars        
            with st.chat_message("user", avatar="🧔‍♂️"):
                st.markdown(user_input)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(result["answer"])

