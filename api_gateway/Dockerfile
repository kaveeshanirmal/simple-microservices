FROM python:3.12-slim

WORKDIR /app

COPY shared/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY api_gateway/config.py config.py
COPY api_gateway/main.py main.py

ENV SERVICE_STATE=healthy

EXPOSE 8104

CMD ["gunicorn", "--bind", "0.0.0.0:8104", "--workers", "2", "--access-logfile", "-", "main:app"]
