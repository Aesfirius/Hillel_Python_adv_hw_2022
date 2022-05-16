FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update
RUN apt -y install ffmpeg

RUN pip3 install -r requirements.txt

COPY . .
