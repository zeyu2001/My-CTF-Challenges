FROM node:17-alpine

RUN apk update && \
apk add --no-cache chromium dumb-init

ENV NODE_ENV=production \
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
PUPPETEER_EXECUTABLE_PATH=/usr/lib/chromium/chrome

RUN addgroup inmate && \
adduser --disabled-password --gecos "" --ingroup inmate inmate

WORKDIR /home/inmate/app
COPY . ./

RUN chown -R inmate:inmate .
USER inmate
RUN npm install && \
mkdir -p /home/inmate/Downloads

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "./main.js"]