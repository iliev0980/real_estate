FROM python:3.9.5-alpine

# set work directory
WORKDIR /usr/src/real_estate

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev && apk add bash

ENV TZ=Europe/Sofia
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN  pip install -r requirements.txt

COPY . /real_estate

# run entrypoint.sh
ENTRYPOINT ["/usr/src/real_estate/entrypoint.sh"]