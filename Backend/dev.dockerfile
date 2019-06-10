# Instalación de Python (SLIM)
FROM python:3.6.8-slim as python

# Actualizar apt-get
RUN apt-get update

# Instalar sudo
RUN apt-get install sudo -y

# Instalar bash
RUN sudo apt-get install bash

# Instalar add-apt-repository
RUN apt-get install software-properties-common -y

# Agregar repositorio para instalar libjasper-dev
#RUN sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"

# Instalar dependencias
RUN sudo apt-get install build-essential -y
RUN sudo apt-get install cmake -y
RUN sudo apt-get install git -y
RUN sudo apt-get install libgtk2.0-dev -y
RUN sudo apt-get install pkg-config -y
RUN sudo apt-get install libavcodec-dev -y
RUN sudo apt-get install libavformat-dev -y
RUN sudo apt-get install libswscale-dev -y
RUN sudo apt-get install libtbb2 -y
RUN sudo apt-get install libtbb-dev -y
RUN sudo apt-get install libjpeg-dev -y
RUN sudo apt-get install libpng-dev -y
RUN sudo apt-get install libtiff-dev -y
#RUN sudo apt-get install libjasper-dev -y
RUN sudo apt-get install libdc1394-22-dev -y

# Copiar requirements.txt
COPY requirements.txt /usr/src/backend/

# Cambiar directorio
WORKDIR /usr/src/backend/

# Instalar dependencias
RUN pip3 install -r requirements.txt