# pull official base image
FROM python:3.8.5

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt .
run pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# copy project
COPY ./ .
COPY /home/ubuntu/BackEnd/db.sqlite3 .