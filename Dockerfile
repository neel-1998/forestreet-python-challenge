FROM python:3.7.4-slim
RUN apt update && apt upgrade -y
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY python-modules ./python-modules
