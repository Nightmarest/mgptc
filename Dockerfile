FROM ubuntu:latest

RUN apt update
RUN apt install python3-pip -y
RUN apt-get install libpq-dev -y
RUN pip3 install aiogtts
RUN pip3 install uvicorn
RUN pip3 install fastapi==0.103.1
RUN pip3 install discum
RUN pip3 install redis
RUN pip3 install aiocron
RUN pip3 install Levenshtein
RUN pip3 install asyncpg
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Yekaterinburg
RUN apt-get install -y tzdata
RUN pip3 install python-multipart
RUN pip3 install python-dateutil
RUN pip3 install typing_extensions
RUN pip3 install fake_useragent
#RUN pip3 install flask[async]
RUN pip3 install pyCryptomusAPI
WORKDIR /usr/app/src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
