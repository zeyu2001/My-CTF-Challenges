FROM python:3.9.5-slim-buster

WORKDIR /opt/rocket_science

COPY rocket_science.py /opt/rocket_science

COPY requirements.txt /opt/rocket_science

COPY flag.txt /opt/rocket_science

RUN apt update

RUN apt install -y \
    python \
    socat

RUN pip install -r requirements.txt &&\
    useradd -m rocket_science

USER rocket_science

EXPOSE 5000

ENTRYPOINT socat tcp-l:5000,fork,reuseaddr exec:./rocket_science.py