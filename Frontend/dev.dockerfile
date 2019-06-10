# Node 8.15.1
FROM node:10.16.0-alpine

# Instalar bash
RUN apk update && apk add bash

# Instalar @angular/cli
RUN npm install -g @angular/cli@8.0.2

# Crear carpeta /usr/src/frontend
RUN mkdir -p /usr/src/frontend

# Ubicarse en carpeta /usr/src/frontend
WORKDIR /usr/src/frontend

# Copiar package.json y package-lock.json
COPY package*.json /usr/src/frontend/

# Instalar dependencias de package.json
RUN npm install