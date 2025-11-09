FROM ubuntu:latest
LABEL authors="ollie"

RUN apt-get update
RUN apt-get install -y python3.12.0 python3-pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY main.py /opt/main.py

ENTRYPOINT FLASK_APP=/opt/main.py flask run -- host=0.0.0.0