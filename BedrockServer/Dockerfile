# Docker container for a Minecraft Server
# https://minecraft.net/download
#
# Build from lastest stable source code


FROM ubuntu:18.04
MAINTAINER Alan Wakeford <alan.wakeford@gmail.com>

ENV PKGS vim screen rsync zip wget curl 

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y $PKGS && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c "wget https://minecraft.azureedge.net/bin-linux/bedrock-server-1.11.2.1.zip; \
                  unzip bedrock-server-1.11.2.1.zip -d BedrockServer; \
                  rm -f bedrock-server-1.11.2.1.zip;"
EXPOSE 19132 

ADD startup.sh /startup.sh
CMD ["/bin/bash", "/startup.sh"]

