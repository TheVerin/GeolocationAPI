# Pull base image
FROM python:3.7-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create directory for the specialuser
RUN mkdir /app

# create the appropriate directories
ENV APP_ROOT=/app
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
