FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080
ENV DEBUG=1
ENV DJANGO_ALLOWED_HOSTS='127.0.0.1 localhost'
ENV DATABASE='postgres'

ENV SQL_ENGINE=django.db.backends.postgresql
ENV SQL_DATABASE=grouper
ENV SQL_USER=admin
ENV SQL_PASSWORD=admin
ENV SQL_HOST=db
ENV SQL_PORT=5432

RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        netcat \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip


WORKDIR /code

ADD requirements.txt /code/

RUN pip3 install -r requirements.txt

ADD . /code/

EXPOSE 8080

ENTRYPOINT ["/code/entrypoint.sh"]