from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_core.tools import Tool
import pandas as pd
import tempfile
import os

llm = ChatGroq(model="llama3-8b-8192", temperature=0.5, verbose=True)
# llm = ChatOllama(model="llama3.1", temperature=0, verbose=True)

# Sets up embedding model (HuggingFace)
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def csv_agent(csv_path):
    if csv_path is not None:
        try:
            # Handles csv file uploads via temporary files
            content = csv_path.read()
            with tempfile.NamedTemporaryFile("wb", suffix="csv", delete=False) as temp_csv:
                temp_csv.write(content)
                temp_csv_path = temp_csv.name

            # Now read from this temp file
            df = pd.read_csv(temp_csv_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(temp_csv_path, encoding='cp1252')

        df = df.dropna(how='all').dropna(axis=1, how='all')
        # Create the agent
        agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=True, allow_dangerous_code=True)
        
        # Clean up the buffer file
        try:
            os.unlink(temp_csv_path)
        except:
            pass
        
        return agent


## Text Agent
def text_agent(text_path, top_k=5):
    if text_path is not None:
        # Handles text file uploads via temporary files
        content = text_path.read()
        with tempfile.NamedTemporaryFile("wb", suffix="txt", delete=False) as temp_txt:
            temp_txt.write(content)
            temp_txt_path = temp_txt.name
        
        # Load and process the file
        text_doc = TextLoader(temp_txt_path, encoding="utf-8").load()
        # Splits text into chunks and creates FAISS vector store
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(text_doc)
        text_vectorDB = FAISS.from_documents(text_splitter, embed_model)
        # Returns a retriever for semantic search
        text_retriever = text_vectorDB.as_retriever(search_kwargs={"k": top_k})
        
        # Clean up the temporary file
        try:
            os.unlink(temp_txt_path)
        except:
            pass
        
        return text_retriever

## PDF Agent
def pdf_agent(pdf_path, top_k=3):
    if pdf_path is not None:
        # Processes PDF uploads via temporary files
        content = pdf_path.read()
        with tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Load and process the file
        pdf_doc = PyPDFLoader(temp_path).load()
        # Splits PDF content and creates Chroma vector store
        pdf_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(pdf_doc)
        pdf_vectorDB = FAISS.from_documents(pdf_splitter, embed_model)
        # Returns a retriever for document search
        pdf_retriever = pdf_vectorDB.as_retriever(search_kwargs={"k": top_k})
        
        # Clean up the temporary file
        try:
            os.unlink(temp_path)
        except:
            pass
       
        return pdf_retriever

## Tool Stores
def get_tools(csv, text, pdf):
    # Dynamically creates tools based on uploaded files
    tools = []

    if csv:
        tools.append(Tool(name="CSV Tool", func=csv_agent(csv).invoke, description="Analyze, Summerize and answer questions from csv file using CSV Tool."))
        
    if text:
        tools.append(Tool(name="Text Tool", func=text_agent(text).get_relevant_documents, description="Search and retrieve relevant text from text file using Text Tool."))
       
    if pdf:
        tools.append(Tool(name="PDF Tool", func=pdf_agent(pdf).get_relevant_documents, description="Extract and search content from PDF files efficiently using PDF Tool."))
        
    return tools