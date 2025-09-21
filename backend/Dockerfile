FROM python:3.9-bullseye

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-nanum \
    --no-install-recommends

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .