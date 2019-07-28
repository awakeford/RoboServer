#!/bin/bash

# git clone https://github.com/DockerDemos/MinecraftServer.git
cd MinecraftServer

sudo docker build -t minecraft .

sudo docker run \
	-p 25565:25565 \
        --name minecraft \
	--mount type=bind,source=$(pwd)/servers,target=/opt/msm/servers \
	--restart unless-stopped \
	-d minecraft

#sudo docker exec -it minecraft  bash
