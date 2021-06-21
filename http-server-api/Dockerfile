FROM python:3.7-slim-buster

WORKDIR /app
COPY src .
ADD requirements.txt .
RUN pip3 install -r requirements.txt
CMD python3 entrypoint.py
