FROM python:3.7

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD * /app/
WORKDIR /app/

ENV PYTHONUNBUFFERED=1

ENTRYPOINT gunicorn --timeout=480 --keep-alive=480 app:app --access-logfile '-' -b 0.0.0.0:8080