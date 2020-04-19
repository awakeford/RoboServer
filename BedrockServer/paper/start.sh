#!/bin/sh
############################################################
#a Java Minecraft start script
###########################################################

##########################################################3
# Copies all files needed to/from the world and starts
# Minecraft
###########################################################

cp_file () {

   if [[ -e ./${WORLD}/$1 ]]; then
     echo "Using ./${WORLD}/$1"  
   elif [[ -e ../RoboServer/java/$1 ]]; then
     echo "Getting RoboServer/$1"
     cp -fr ../RoboServer/java/$1 ./${WORLD}/
   elif [[ -e $1 ]]; then
     echo "Using default $1"
     cp -fr $1 ./${WORLD}/$1
   fi

   if [[ -e $1 ]]; then
     mv -f $1 ./${WORLD}/origional/
   fi

   ln -s ./${WORLD}/$1 ./ 
}

get_config() {

  echo "world is ${WORLD}" 
  
  if [[ ! -e ../RoboServer/worlds/${WORLD} ]]; then
     mkdir ../RoboServer/worlds/${WORLD}
     mkdir ../RoboServer/worlds/${WORLD}/origional    
     mkdir ../RoboServer/worlds/${WORLD}/logs 
  fi
      	  
  if [[ -e ${WORLD} ]]; then
     rm -fr ${WORLD}
  fi

  ln -s ../RoboServer/worlds/${WORLD} ./

  #mv server.properties server.properies.old
  cp_file "server.properties"
  cp_file "whitelist.json"
  cp_file "ops.json"
  cp_file "logs"
  cp_file "banned-players.json"
  cp_file "banned-ips.json"
  cp_file "eula.txt"
  cp_file "plugins"

  # Make sure that world files have the correct server/level name
  sed -i s/"server-name=.*"/"server-name=${WORLD}"/g            server.properties
  sed -i s/"level-name=.*"/"level-name=${WORLD}"/g              server.properties
  sed -i s/"white-list=.*"/"white-list=true"/g                  server.properties
  sed -i s/"enforce-whitelist=.*"/"enforce-whitelist=true"/g    server.properties
}

get_config
exec java -Xmx${JAVA_XMX} -jar /usr/local/bin/server.jar --port ${PORT} nogui

