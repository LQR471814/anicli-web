FROM python:3.11-alpine

WORKDIR /app

RUN pip install anipy-cli bottle
COPY ./server.py /app/server.py
COPY ./static /app/static
COPY ./views /app/views

ENV IMAGEIO_FFMPEG_EXE="/ffmpeg"

CMD ["python3", "/app/server.py"]

