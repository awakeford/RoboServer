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
	&& curl -L -o /usr/local/bin/server.jar \
                https://papermc.io/api/v1/paper/1.15.2/193/download

# -------------------------------------------------------------------------------------------------
# Final Docker image
# -------------------------------------------------------------------------------------------------
FROM openjdk:${JAVA_VERSION}-alpine as production
ARG SERVER_VERSION=1.15.2

###
### Copy from builder
###
COPY --from=builder /usr/local/bin/server.jar /usr/local/bin/server.jar
RUN mkdir /data

###
### Server default settings
###
ENV SERVER_VERSION=${SERVER_VERSION}
ENV PORT=25565
ENV JAVA_XMX=1536M

###
### Persistant data
###
#VOLUME ["/data"]

###
### Startup
###
WORKDIR /data
CMD ["../RoboServer/paper/start.sh"]
