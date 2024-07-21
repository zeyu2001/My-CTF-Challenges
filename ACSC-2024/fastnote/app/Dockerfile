FROM golang:1.20.13

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

RUN mkdir /app
RUN chmod -R 705 /app

WORKDIR /app

COPY server .
COPY static ./static
COPY templates ./templates

RUN go mod download
RUN go build -o main .

RUN groupadd -g 1000 ctf
RUN useradd -g ctf -s /bin/bash ctf

USER ctf

CMD ["./main"]