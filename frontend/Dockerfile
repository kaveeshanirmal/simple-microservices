FROM python:3.12-slim

WORKDIR /app

COPY shared/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY frontend/config.py config.py
COPY frontend/main.py main.py

ENV SERVICE_STATE=healthy

EXPOSE 8100

CMD ["gunicorn", "--bind", "0.0.0.0:8100", "--workers", "2", "--access-logfile", "-", "main:app"]
