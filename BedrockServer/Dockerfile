# Docker container for a Minecraft Server
# https://minecraft.net/download
#
# Build from lastest stable source code


FROM ubuntu:18.04
MAINTAINER Alan Wakeford <alan.wakeford@gmail.com>

ENV PKGS vim screen rsync zip wget curl netcat python3-minimal python3-pip python3-cherrypy3
ENV VER 1.14.0.9

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y $PKGS && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 

ADD python_requirements.txt /python_requirements.txt
RUN pip3 install -r python_requirements.txt

RUN /bin/bash -c "wget https://minecraft.azureedge.net/bin-linux/bedrock-server-${VER}.zip; \
                  unzip bedrock-server-${VER}.zip -d BedrockServer; \
                  rm -f bedrock-server-${VER}.zip;"

EXPOSE 19132/udp 19133/udp
 
CMD ["/bin/bash", "BedrockServer/RoboServer/startup.sh"]

