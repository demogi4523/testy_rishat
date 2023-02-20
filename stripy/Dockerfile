FROM python:3.7-slim-buster

SHELL ["/bin/bash", "-c"]

# set work directory
# WORKDIR /usr/src/app
WORKDIR /code

# set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY stripy/ .
COPY create_config.sh .
COPY start.sh .
RUN source create_config.sh

EXPOSE 8000

# CMD ["gunicorn", "stripy.wsgi:application", "--bind", "0.0.0.0:8000"]
