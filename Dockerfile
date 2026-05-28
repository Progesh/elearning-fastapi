FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8081

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8081", "--reload"]
