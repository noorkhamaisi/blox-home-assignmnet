# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster

EXPOSE 5005


RUN pip install --upgrade pip

#install curl
RUN apt-get update
RUN apt-get install -y curl

ADD requirements.txt .

RUN apt-get update && apt-get install -y build-essential
RUN pip install -r requirements.txt




WORKDIR /app
ADD . /app


CMD ["python3",  "blocks_assignmnet.py"]