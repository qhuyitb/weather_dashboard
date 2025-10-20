# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Mở port Streamlit
EXPOSE 8501

# Chạy Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
