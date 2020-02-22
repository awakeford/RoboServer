#!/usr/bin/python3

import json
import subprocess
import os
import docker

# Get the docker client API
client = docker.from_env()

mc_ports = (19132,19133)

def build():
   print("Building bedrock image") 
   (image,build_log) = client.images.build(path="./",tag="bedrock") 
   for l in build_log:
       print(l)

def container(name):
   container = None
   try:
      container = client.containers.get(name)
   except docker.errors.NotFound:
      print("No container named",name)

   return container

def stop(name):
   c = container(name)
   if c:
      print("Stopping",name) 
      c.remove(force=True)

def start(name,mc_ports,web_port,local_log):

   print("Starting",name) 
   c = client.containers.run('bedrock',
                             name=name,                             
                             ports={'19132/udp' : mc_ports[0],
                                    '19133/udp' : mc_ports[1],
                                    '80/tcp'    : web_port},
                             mounts=[docker.types.Mount(target='/BedrockServer/RoboServer', source=os.getcwd(), type='bind')],
                             restart_policy={'Name' : 'on-failure'},
                             detach=True,
                             environment={'WORLD' : name,"LOCAL_LOG" : local_log})

def containers():
    return client.containers.list()

if __name__== "__main__":
   import argparse

   parser = argparse.ArgumentParser(description='Arguments.')
   parser.add_argument('-w','--world', dest="world", action="store",
                       help='World')
   parser.add_argument('-p','--mc_ports', dest="mc_ports", action="append", nargs=2, type=int,
                       help='Minecraft ports %d %d' % mc_ports)
   parser.add_argument('-o','--web_port', dest="web_port", action="store", default="80",
                       help='WebServer port')
   parser.add_argument('-s','--stop', dest="stop", action="store_true", 
                       help='Stop running container')
   parser.add_argument('-b','--build', dest="build", action="store_true",
                       help='Build docker image')
   parser.add_argument('-r','--run', dest="run", action="store_true",
                       help='Run docker container')
   parser.add_argument('-j','--join', dest="join", action="store_true",
                       help='Join running world container (bash)')
   parser.add_argument('-l','--list', dest="list", action="store_true",
                       help='List world status')

   args = parser.parse_args()

   if not args.mc_ports:
      args.mc_ports = mc_ports
   else:
      args.mc_ports = args.mc_ports[0]

   if args.list:
       for c in containers():
           print(c.name)

   if not args.world:
      try:
         args.world = containers()[0].name
         print("Using world",args.world) 
      except IndexError:
         raise LookupError("No running worlds, must supply world")

   if args.stop or args.run:       
      stop(args.world)

   if args.build:
      build()

   if args.run: 
      start(args.world,args.mc_ports,args.web_port, local_log = containers() and "TRUE" or "FALSE")

   if args.join:
      world_container = container(args.world)
      if world_container:
         world_container.exec_run(cmd="bash",tty=True,stdin=True,stdout=True,stderr=True)

# sudo docker exec -it bedrock bash
# sudo docker stats bedrock
# sudo attach bedrock
