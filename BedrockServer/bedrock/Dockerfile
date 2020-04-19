# Docker container for a Minecraft Server
# https://minecraft.net/download
#
# Build from lastest stable source code

FROM ubuntu:18.04 as builder
MAINTAINER Alan Wakeford <alan.wakeford@gmail.com>

ENV VER 1.14.32.1

ENV PKGS wget zip curl

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y $PKGS && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

RUN /bin/bash -c "wget https://minecraft.azureedge.net/bin-linux/bedrock-server-${VER}.zip; \
                  unzip bedrock-server-${VER}.zip -d data;"

FROM ubuntu:18.04 as producer

ENV PKGS curl

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y $PKGS && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /data /data

EXPOSE 19132/udp 
 
WORKDIR /data
CMD ["../RoboServer/bedrock/start.sh"]
