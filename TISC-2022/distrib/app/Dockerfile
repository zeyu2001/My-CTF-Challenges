FROM node:16.3.0

RUN apt-get update && \
apt-get install -y chromium dumb-init xvfb && \
rm -rf /var/lib/apt/lists/*

ENV NODE_ENV=production \
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

RUN addgroup inmate && \
adduser --disabled-password --gecos "" --ingroup inmate inmate

WORKDIR /home/inmate/app
COPY . ./

RUN chmod +x ./start.sh

RUN chown -R inmate:inmate .
USER inmate
RUN npm install && \
mkdir -p /home/inmate/Downloads

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["./start.sh"]
