FROM python:3.12-slim

WORKDIR /app

COPY shared/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY payment/config.py config.py
COPY payment/main.py main.py

ENV SERVICE_STATE=healthy

EXPOSE 8102

CMD ["gunicorn", "--bind", "0.0.0.0:8102", "--workers", "2", "--access-logfile", "-", "main:app"]
