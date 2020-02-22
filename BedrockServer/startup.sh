#!/bin/bash
############################################################
#a Bedrock start script
#
# Copies all files needed to/from the world and starts
# bedrock.
###########################################################


cp_file () {

   if [[ -e ./worlds/${WORLD}/$1 ]]; then
     echo "Using ./worlds/${WORLD}/$1" >> local.log 
   elif [[ -e RoboServer/$1 ]]; then
     echo "Getting RoboServer/$1"  >> local.log
     cp -fr RoboServer/$1 ./worlds/${WORLD}/
   elif [[ -e $1 ]]; then
     echo "Using default $1" >> local.log
     cp -fr $1 ./worlds/${WORLD}/$1
   fi

   if [[ -e $1 ]]; then
     rm -fR $1
   fi  

   ln -s ./worlds/${WORLD}/$1 ./ 
}

get_config() {

  touch local.log

  echo "world is ${WORLD}" >> local.log
  mkdir worlds
  if [[ ! -e ./RoboServer/worlds/${WORLD} ]]; then
     mkdir ./RoboServer/worlds/${WORLD}	  
  fi
      	  
  ln -s ../RoboServer/worlds/${WORLD} ./worlds/

  #ls -alF        >> local.log
  #ls -alf worlds >> local.log

  #mv server.properties server.properies.old
  #cp -fR RoboServer/server.properties ./
  cp_file "server.properties"
  cp_file "permissions.json"
  cp_file "whitelist.json"
  cp_file "server.log"
  cp_file "web_server.log"
  #cp_file "resource_packs"
  #cp_file "behavior_packs"
  cp_file "world_resource_packs.json"
  cp_file "world_behavior_packs.json"

  cat local.log >> server.log
  rm -fR local.log

  cp -fR worlds/${WORLD}/resource_packs/* resource_packs/
  cp -fR worlds/${WORLD}/behavior_packs/* behavior_packs/
  #cp worlds/${WORLD}/world_resource_packs.json ./
  #cp worlds/${WORLD}/world_behavior_packs.json ./

  # Make sure that world files have the correct server/level name
  sed -i s/"server-name=.*"/"server-name=${WORLD}"/g server.properties
  sed -i s/"level-name=.*"/"level-name=${WORLD}"/g   server.properties
}

cd BedrockServer
get_config
python3 RoboServer/web_server.py   |& tee -a web_server.log &
LD_LIBRARY_PATH=. ./bedrock_server |& tee -a server.log
#sleep 1h

