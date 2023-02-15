FROM node:14-alpine AS base
USER node
WORKDIR /app
COPY ./"webpack.config.js" /app
COPY ./"package.json" /app
RUN npm install
COPY ./assets /app/assets