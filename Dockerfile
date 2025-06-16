FROM python:3.11

EXPOSE 8080
WORKDIR /app

# RUN mkdir -p /app/model_cache && chmod -R 777 /app/model_cache

# ENV TRANSFORMERS_CACHE=/app/model_cache
# ENV HF_HOME=/app/model_cache
# ENV XDG_CACHE_HOME=/app/model_cache

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Pre-download the embedding model
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', cache_folder='/app/model_cache')"

COPY . ./

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
