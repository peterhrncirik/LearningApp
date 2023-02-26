# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `app`
RUN mkdir -p /app
RUN mkdir -p /app/staticfiles
WORKDIR /app

# Install dependencies
COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y ffmpeg && \
    rm -rf /root/.cache/ 

# Copy local project
COPY . /app/
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
