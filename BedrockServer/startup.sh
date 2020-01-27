#!/bin/bash

cp_file () {
   if [[ -e RoboServer/$1 ]]; then
     echo "Getting RoboServer/$1"	  
     rm -fR $1 
   elif [[ -e $1 ]]; then
     echo "Saving RoboServer/$1"	   
     mv $1 RoboServer/	   
   else
     echo "New RoboServer/$1"	   
     touch RoboServer/$1
   fi

   ln -s RoboServer/$1 ./ 
}

get_config() {

  cp_file "server.properties"
  cp_file "permissions.json"
  cp_file "whitelist.json"
  cp_file "worlds"
  cp_file "server.log"
  cp_file "web_server.log"

  world="$(grep level-name server.properties | sed s/level-name=//g)"

  cp -fR worlds/${world}/resource_packs/* resource_packs/
  cp -fR worlds/${world}/behavior_packs/* behavior_packs/
  cp worlds/${world}/world_resource_packs.json ./
  cp worlds/${world}/world_behavior_packs.json ./

  echo "world is ${world}" >> server.log
}	

cd BedrockServer
get_config
python3 RoboServer/web_server.py |& tee -a web_server.log &
LD_LIBRARY_PATH=. ./bedrock_server |& tee -a server.log
#sleep 1h

