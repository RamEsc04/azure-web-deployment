FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/app.py .

EXPOSE 5000

ENV APP_ENV=dev
ENV APP_VERSION=1.0.0-dev

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]