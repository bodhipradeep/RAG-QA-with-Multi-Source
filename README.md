# RAG QA Chatbot with Multi‑Source Support

This repository implements a **Retrieval‑Augmented Generation (RAG)** chatbot built in Python, deploying a Streamlit-based UI to answer user queries from multiple document sources (PDF, TXT, CSV) using semantic search (via FAISS) and a language model (Groq or Ollama). Deployed on AWS and containerized via Docker.

---

## 🔧 Features & Flow Overview

1. **Document ingestion** – Users can upload PDF, TXT, or (commented) CSV.  
2. **Preprocessing** – Files are parsed, split into chunks, and embedded using HuggingFace models.  
3. **Vector store retrieval** – Stores embeddings in FAISS for semantic search.  
4. **RAG pipeline** – Top chunks retrieved and fed into an LLM (ChatGroq) via a prompt template.  
5. **Streamlit frontend** – Provides conversational UI for users.  
6. **Deployment-ready** – Containerized using Docker. Tested on AWS EC2 with complete deploy instructions.

---
## Sample Image of output
<p align="center">
  <img src="https://github.com/user-attachments/assets/ad105f48-54a7-4a2c-9106-86527d06e4e3" alt="Deploying" width="45%" /> 
  &nbsp;&nbsp;&nbsp;
  <img src="https://github.com/user-attachments/assets/55fc3ee6-70af-4276-91bb-94214706be77" alt="Running" width="45%" />
</p>
---

## 🚀 Quick Start

### Clone
```bash
git clone https://github.com/bodhipradeep/RAG-QA-with-Multi-Source.git
cd RAG-QA-with-Multi-Source
```

## Install dependencies
```bash
pip install -r requirements.txt
```
## Run locally
```bash
streamlit run main.py
```
--- 
# AWS EC2 Deployment (already implemented)

```bash
sudo yum update -y
sudo yum install git pip -y
git clone https://github.com/bodhipradeep/RAG-QA-with-Multi-Source.git
cd RAG-QA-with-Multi-Source
pip install -r requirements.txt
streamlit run main.py
```

Access via EC2 public IP and port 8501.
[AWS Complete Guide](AWS_DEPLOYMENT.md)

---

## 📂 Sample Documents & Test Workflow
- Sample PDF/TXT files are located in the repo under sample_data/.
- A Jupyter Notebook (text.ipynb) demonstrates ingestion and queries.
- Upload files via the Streamlit UI and observe instant answers.

---

### Project Structure
```bash
├─ app.py             # Streamlit application
├─ retriever.py        # Parsing, embedding, FAISS indexing
├─ requirements.txt    # Dependencies
├─ Dockerfile          # Container setup
├─ text.ipynb          # Sample ingestion & testing notebook
└─ source_data.zip/    # Example PDF & TXT files
```
---

### Usage Examples (Streamlit UI)
- Upload one or more documents (PDF/TXT).
- Enter your question (e.g., “What is the objective of the project?”).
- Expect conversational answers based on content.
- Monitor console logs for processing feedback.

---

## 📄 License

This repository is licensed under the MIT License. See the LICENSE file for details.

--- 

## 🔗 **Links & Contact**

- **GitHub Profile:** [Github](https://github.com/pradeep-kumar8/)
- **LinkedIn:** [Likedin](https://linkedin.com/in/pradeep-kumar8)
- **Email:** [gmail](mailto:pradeep.kmr.pro@gmail.com)
