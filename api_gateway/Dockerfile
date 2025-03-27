FROM python:3.10-slim

WORKDIR /app

# Copy only the necessary app files
COPY api_gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_gateway . 
COPY database ./database

CMD ["python", "app.py"]
