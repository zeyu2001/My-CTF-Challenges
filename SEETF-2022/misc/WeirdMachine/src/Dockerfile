FROM python:3

RUN useradd -m chall

RUN apt update

RUN apt install -y \
    socat

COPY service.py /opt/app/service.py
RUN chmod +rx /opt/app/service.py

WORKDIR /opt/app/

USER chall

ENTRYPOINT socat tcp-l:5000,fork,reuseaddr exec:./service.py