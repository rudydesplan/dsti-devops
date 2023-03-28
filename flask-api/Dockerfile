FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY modules /app/modules
COPY service /app/service

EXPOSE 5000

ENV PYTHONPATH="${PYTHONPATH}:/app/modules"

CMD ["python", "service/service.py"]

