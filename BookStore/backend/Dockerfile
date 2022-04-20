FROM ubuntu:16.04

RUN apt-get update
RUN apt -y install build-essential
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get -y install nodejs
RUN apt-get install --no-install-recommends apt-utils --yes \
    && apt-get install --no-install-recommends npm --yes \
    && apt-get install --no-install-recommends node --yes

RUN npm install
RUN node server.js