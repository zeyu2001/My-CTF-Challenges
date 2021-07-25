FROM python:3.9.5-slim-buster

WORKDIR /opt/rocket_ship_academy

COPY rocket_ship_academy.py /opt/rocket_ship_academy

COPY requirements.txt /opt/rocket_ship_academy

COPY flag.txt /opt/rocket_ship_academy

RUN apt update

RUN apt install -y \
    python \
    socat

RUN pip install -r requirements.txt &&\
    useradd -m rocket_ship_academy

USER rocket_ship_academy

EXPOSE 5000

ENTRYPOINT socat tcp-l:5000,fork,reuseaddr exec:./rocket_ship_academy.py