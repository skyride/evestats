FROM python:3.6-alpine

# Set up envrionment
WORKDIR /app

COPY requirements.txt /app
RUN apk update && \
    apk add postgresql-libs && \
    apk add --virtual .builds-deps gcc musl-dev postgresql-dev ca-certificates wget && \
    update-ca-certificates && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV THREADS=3

CMD gunicorn -w $THREADS -b 0.0.0.0:8000 evestats.wsgi:application