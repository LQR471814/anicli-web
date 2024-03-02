FROM python:3.11-alpine

WORKDIR /app

RUN apk add clang musl-dev ffmpeg
RUN pip install anipy-cli bottle
COPY ./server.py /app/server.py
COPY ./static /app/static
COPY ./views /app/views

CMD ["python3", "/app/server.py"]

