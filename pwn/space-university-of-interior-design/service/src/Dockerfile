FROM debian:latest

WORKDIR /home

COPY flag.txt /root

RUN apt update

RUN apt-get update && apt install -y \
    gcc-multilib \
    socat \
    python3

RUN apt-get install -y sudo
RUN apt-get install -y sqlite3

COPY sudoers /etc

RUN useradd -m jared
RUN useradd -m guest
RUN usermod -aG sudo jared

COPY chinook.db /home/jared
COPY query_db.py /home/jared
COPY creds.txt /home/jared

COPY passwd /etc

RUN chown -R jared:jared .
RUN chmod +x /home/jared/query_db.py

RUN chmod -R 700 /home/jared
RUN chmod -R 700 /home/guest

RUN chown jared /usr/bin/python3
RUN chmod 4755 /usr/bin/python3

USER jared

USER guest

EXPOSE 5000

ENTRYPOINT socat tcp-l:5000,fork,reuseaddr exec:"/bin/bash -i"