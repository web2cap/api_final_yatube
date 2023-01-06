FROM python:3.7-slim

WORKDIR /app
COPY yatube_project/ .
RUN pip3 install -r requirements.txt --no-cache-dir



CMD ["gunicorn", "yatube.wsgi:application", "--bind", "0:8000" ]