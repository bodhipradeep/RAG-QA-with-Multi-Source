from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
import tempfile
import os

# Sets up embedding model (HuggingFace)
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

## retriever
def retriever(text, pdf, top_k=5):
    if text or pdf is not None:
        # Handles text file uploads via temporary files
        content = text.read()
        with tempfile.NamedTemporaryFile("wb", suffix="txt", delete=False) as temp_txt:
            temp_txt.write(content)
            temp_txt_path = temp_txt.name
        
        # Processes PDF uploads via temporary files
        content = pdf.read()
        with tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Load and process the file
        text_doc = TextLoader(temp_txt_path, encoding="utf-8").load()
        pdf_doc = PyPDFLoader(temp_path).load()
        
        document = text_doc+pdf_doc
        
        # Splits text into chunks and creates FAISS vector store
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(document)
        vectorstore = FAISS.from_documents(splitter, embed_model)
        # Returns a retriever for semantic search
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        
        #Clean up the buffer file
        try:
            os.unlink(temp_txt_path)
            os.unlink(temp_path)
        except:
            pass

        return retriever


# def csv_agent(csv_path, llm):
#     if csv_path is not None:
#         try:
#             # Handles csv file uploads via temporary files
#             content = csv_path.read()
#             with tempfile.NamedTemporaryFile("wb", suffix="csv", delete=False) as temp_csv:
#                 temp_csv.write(content)
#                 temp_csv_path = temp_csv.name

#             # Now read from this temp file
#             df = pd.read_csv(temp_csv_path, encoding='utf-8')
#         except UnicodeDecodeError:
#             df = pd.read_csv(temp_csv_path, encoding='cp1252')

#         df = df.dropna(how='all').dropna(axis=1, how='all')
#         # Create the agent
#         agent = create_pandas_dataframe_agent(llm=llm, df=df, verbose=True, allow_dangerous_code=True)
        
#         # Clean up the buffer file
#         try:
#             os.unlink(temp_csv_path)
#         except:
#             pass
        
#         return agent.run
