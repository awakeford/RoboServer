ARG JAVA_VERSION=14
# -------------------------------------------------------------------------------------------------
# Builder Docker image
# -------------------------------------------------------------------------------------------------
FROM openjdk:${JAVA_VERSION}-alpine as builder
ARG SERVER_VERSION=1.15.2

###
### Install Server
###
RUN set -eux \
	&& apk add --no-cache curl \
	&& curl -L -o /usr/local/bin/server-${SERVER_VERSION}.jar \
                'https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar'

# -------------------------------------------------------------------------------------------------
# Final Docker image
# -------------------------------------------------------------------------------------------------
FROM openjdk:${JAVA_VERSION}-alpine as production
ARG SERVER_VERSION=1.15.2

###
### Copy from builder
###
COPY --from=builder /usr/local/bin/server-${SERVER_VERSION}.jar /usr/local/bin/server-${SERVER_VERSION}.jar
RUN mkdir /data

###
### Server default settings
###
ENV SERVER_VERSION=${SERVER_VERSION}
ENV PORT=25565
ENV JAVA_XMX=4096M

###
### Persistant data
###
#VOLUME ["/data"]

###
### Startup
###
WORKDIR /data
CMD ["../RoboServer/java/start.sh"]
