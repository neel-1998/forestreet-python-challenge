FROM python:3.7.4-slim as base
RUN apt update && apt upgrade -y
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY python_modules ./python_modules

# FROM base as test
# COPY requirements-dev.txt ./
# RUN pip install -r requirements-dev.txt
# COPY test ./test
# RUN python -m pytest -v
