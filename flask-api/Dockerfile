FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt setup.py .
COPY modules ./modules
COPY service ./service

RUN pip install --no-cache-dir -r requirements.txt &&\
    python setup.py install

EXPOSE 5000

CMD ["python", "service/service.py"]
