FROM python:3.11

EXPOSE 8080
WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . ./

# ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
CMD streamlit run --server.port 8080 --server.enableCORS false app.py