FROM python:3.12-slim

WORKDIR /app

COPY shared/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY auth/config.py config.py
COPY auth/main.py main.py

ENV SERVICE_STATE=healthy

EXPOSE 8101

CMD ["gunicorn", "--bind", "0.0.0.0:8101", "--workers", "2", "--access-logfile", "-", "main:app"]
