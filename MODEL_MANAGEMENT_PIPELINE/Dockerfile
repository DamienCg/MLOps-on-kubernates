FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model_management_pipeline.py .

CMD ["python", "model_management_pipeline.py"]
