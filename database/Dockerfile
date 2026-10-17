FROM python:3.12-slim

WORKDIR /app

COPY shared/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY database/config.py config.py
COPY database/main.py main.py

ENV SERVICE_STATE=healthy

EXPOSE 8105

CMD ["gunicorn", "--bind", "0.0.0.0:8105", "--workers", "2", "--access-logfile", "-", "main:app"]
