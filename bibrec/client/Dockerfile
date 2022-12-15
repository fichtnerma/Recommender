FROM node:latest
WORKDIR /opt/
COPY ./package.json ./
COPY ./package-lock.json ./
ENV PATH /opt/node_modules/.bin:$PATH
RUN yarn config set network-timeout 600000 -g && npm ci
WORKDIR /opt/app
COPY ./ .
EXPOSE 3000
CMD npm run dev
