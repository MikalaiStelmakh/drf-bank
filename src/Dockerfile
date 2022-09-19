FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY ./app /app

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip3 install -r requirements.txt

WORKDIR /app