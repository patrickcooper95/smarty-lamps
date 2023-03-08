FROM python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

# Install gcc compiler for sysv_ipc pip package
RUN apt-get update && apt-get install -y gcc

# Install pip packages
RUN pip install -r requirements.txt

ENV ENVIRONMENT=TEST

COPY . /app

ENTRYPOINT ["python", "run.py"]
