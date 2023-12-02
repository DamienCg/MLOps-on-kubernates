FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Espone la porta 5000
EXPOSE 4949

# Avvia l'applicazione
CMD ["python", "app3.py"]
