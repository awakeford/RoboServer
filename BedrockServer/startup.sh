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
  cp -fR worlds/*/resource_packs/* resource_packs/
  cp worlds/*/*resource*.json resource_packs/
}	

cd BedrockServer
get_config
python3 RoboServer/web_server.py |& tee -a web_server.log &
LD_LIBRARY_PATH=. ./bedrock_server |& tee -a server.log
#sleep 1h

