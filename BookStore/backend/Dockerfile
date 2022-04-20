FROM ubuntu:16.04

RUN apt-get update
RUN apt -y install build-essential
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get -y install nodejs

RUN npm install
RUN node server.js