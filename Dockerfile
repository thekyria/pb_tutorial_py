# syntax=docker/dockerfile:1

ARG CODE_VERSION=latest
FROM kalilinux/kali-rolling:${CODE_VERSION}

LABEL version="1.0" \
    author="thekyria" \
    description="thekyria's kali playground"

SHELL ["/bin/sh", "-c"]

RUN apt -y update && \
    apt -y upgrade && \
    apt install --yes --no-install-recommends \
    procps dos2unix nano bsdmainutils \
    iproute2 iputils-ping tcpdump net-tools \
    python3 python3-pip python-is-python3 \
    protobuf-compiler && \
    apt -y autoclean && apt -y autoremove && apt -y clean

WORKDIR /home/kali

COPY udp_client.py udp_server.py requirements.txt ./
COPY simple_message/ simple_message/
RUN dos2unix ./* simple_message/*

RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install --upgrade -r requirements.txt

RUN protoc --proto_path=. --python_out=simple_message/ simple_message/simple_message.proto