FROM python:3.13

WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY database/confdb.py database/confdb.py
COPY database/models.py database/models.py
COPY config config/
COPY bot bot/

ENV PYTHONPATH=/app
ENV TZ=Europe/Moscow

CMD ["python", "bot/main.py"]