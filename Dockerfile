FROM python:3.12.1-alpine


ENV PYTHONUNBUFFERED 1
COPY requirements.txt /store/
COPY . /store/
WORKDIR /store
EXPOSE 8000

RUN apk add --no-cache postgresql postgresql-client build-base postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password store-user

USER store-user
