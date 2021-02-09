FROM python:buster 
MAINTAINER James Williams <james.williams@packetgeek.net>

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip requests fastapi uvicorn

WORKDIR /opt/bgpstuff/

COPY main.py . 

EXPOSE 8000

CMD uvicorn main:app --reload --host 0.0.0.0 
