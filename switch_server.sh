#!/bin/bash

pushd BedrockServer

current=$(grep level-name server.properties | sed s/level-name=//g)
echo "Current = $current"

sudo docker stop bedrock

if [ "$current" = "BFTTS" ] 
then
  echo "Switch to Trinity"     	
  sudo cp -f trinity_server.properties server.properties
else  
  echo "Swtich to BFTTS"
  if [ -f B.F.T.T.S.zip ]; then
     echo "Installing B.F.T.T.S.zip" 	  
     sudo unzip B.F.T.T.S.zip -o -d worlds/BFTTS
  fi	  
  sudo cp -f bftts_server.properties server.properties
fi

new=$(grep level-name server.properties | sed s/level-name=//g)
echo "new = $new"

sudo docker start bedrock
popd
