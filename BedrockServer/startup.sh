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
     mv -f $1 ./origional/
   fi  

   ln -s ./worlds/${WORLD}/$1 ./ 
}

get_config() {

  mkdir origional	
  touch local.log

  echo "world is ${WORLD}" >> local.log
  mkdir worlds
  if [[ ! -e ./RoboServer/worlds/${WORLD} ]]; then
     mkdir ./RoboServer/worlds/${WORLD}	  
  fi
      	  
  ln -s ../RoboServer/worlds/${WORLD} ./worlds/

  #mv server.properties server.properies.old
  cp_file "server.properties"
  cp_file "permissions.json"
  cp_file "whitelist.json"
  cp_file "server.log"
  cp_file "web_server.log"
  cp_file "world_resource_packs.json"
  cp_file "world_behavior_packs.json"

  cat local.log >> server.log
  rm -fR local.log

  cp -fR worlds/${WORLD}/resource_packs/* resource_packs/
  cp -fR worlds/${WORLD}/behavior_packs/* behavior_packs/

  # Make sure that world files have the correct server/level name
  sed -i s/"server-name=.*"/"server-name=${WORLD}"/g server.properties
  sed -i s/"level-name=.*"/"level-name=${WORLD}"/g   server.properties
}

cd BedrockServer
get_config
LD_LIBRARY_PATH=. ./bedrock_server |& tee -a server.log &
sleep 100d
