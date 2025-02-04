FROM ubuntu:latest
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y python3.8
RUN apt update
RUN apt install python3-pip -y
RUN apt-get install libpq-dev -y
RUN pip3 install aiogtts --break-system-packages
RUN pip3 install uvicorn --break-system-packages
RUN pip3 install fastapi==0.103.1 --break-system-packages
RUN pip3 install discum --break-system-packages
RUN pip3 install redis --break-system-packages
RUN pip3 install aiocron --break-system-packages
RUN pip3 install Levenshtein --break-system-packages
RUN pip3 install asyncpg --break-system-packages
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Yekaterinburg
RUN apt-get install -y tzdata
RUN pip3 install python-multipart --break-system-packages
RUN pip3 install python-dateutil --break-system-packages
RUN pip3 install typing_extensions --break-system-packages
RUN pip3 install fake_useragent --break-system-packages
#RUN pip3 install flask[async] --break-system-packages
RUN pip3 install pyCryptomusAPI --break-system-packages
WORKDIR /usr/app/src

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --break-system-packages
COPY . .
