FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn src.api.server:app --host 0.0.0.0 --port 8000 & streamlit run ui/app.py --server.port 8501 --server.headless true"]
