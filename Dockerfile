FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Definir o PYTHONPATH para que o diretório src seja reconhecido
ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]

#CMD ["fastapi", "run", "main/app", "--host", "0.0.0.0", "--port", "9000", "--workers", "1"]
