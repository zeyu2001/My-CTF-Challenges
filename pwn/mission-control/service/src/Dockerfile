FROM debian:latest

RUN useradd -m mission_control

WORKDIR /home/mission_control

COPY mission_control.c .

COPY flag.txt .

RUN apt update

RUN apt install -y \
    gcc-multilib \
    socat

RUN gcc -static -z execstack -z norelro -fno-stack-protector -o mission_control mission_control.c -m32

RUN chown -R mission_control:mission_control .

USER mission_control

EXPOSE 5000

ENTRYPOINT socat tcp-l:5000,fork,reuseaddr exec:./mission_control