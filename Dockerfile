FROM python:3.12-slim

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["fastapi", "run", "main/app", "--host", "0.0.0.0", "--port", "9000", "--workers", "1"]