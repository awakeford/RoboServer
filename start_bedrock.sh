#!/bin/bash

cd BedrockServer

sudo docker stop bedrock
sudo docker rm bedrock

sudo docker build -t bedrock .

sudo docker run \
	-p 19132:19132/udp \
        -p 19133:19133/udp \
	-p 8080:8080/tcp \
	-p 80:80/tcp \
	--name bedrock \
	--mount type=bind,source=$(pwd),target=/BedrockServer/RoboServer \
	--restart unless-stopped \
	-d bedrock

# sudo docker exec -it bedrock  bash
# sudo docker stats bedrock
# sudo attach bedrock
