FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p static && chmod 777 static
# EXPOSE 80
COPY . .

CMD ["python", "run.py"]