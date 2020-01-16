# Pull base image
FROM python:3.7-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the specialuser
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_ROOT=/home/app/web
RUN mkdir $APP_ROOT
WORKDIR $APP_ROOT

# create the specialuser
RUN addgroup -S specialuser && adduser -S specialuser -G specialuser

# copy dependencies
COPY ./requirements.txt /requirements.txt

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install -r /requirements.txt

# copy project
COPY . $APP_ROOT

# chown all the files to the specialuser
RUN chown -R specialuser:specialuser $APP_ROOT

# change to the specialuser
USER specialuser