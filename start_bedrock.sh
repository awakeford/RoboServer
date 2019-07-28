#!/bin/bash

cd BedrockServer

sudo docker build -t bedrock .

sudo docker run \
	-p 19132:19132 \
	--name bedrock \
	--mount type=bind,source=$(pwd)/servers/RoboServer,target=/BedrockServer/RoboServer \
	--restart unless-stopped \
	-d bedrock
#sudo docker exec -it bedrock  bash

