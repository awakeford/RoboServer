#!/usr/bin/python3

import json
import subprocess
import os
import docker

# Get the docker client API
client = docker.from_env()

config = {"port" : 19132}

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

def ports(container):
   return [int(v[0]['HostPort']) for k,v in container.attrs['NetworkSettings']['Ports'].items()]

def next_port():
    used_prts = []
    for c in containers():
        used_prts.extend(ports(c))
    used_prts.sort()
    if used_prts:
       print(used_prts) 
       free_prts = [p for p in range(config['port'],used_prts[-1]+2) if p not in used_prts]
       return free_prts[0]    
    else: 
       return config['port']

def stop(name):
   c = container(name)
   if c:
      print("Stopping",name) 
      c.remove(force=True)

def start(name,port):

   mounts = [docker.types.Mount(target='/BedrockServer/RoboServer', source=os.getcwd(), type='bind')] 

   ports = {str(config['port'])  + '/udp' : port}

   print("Starting %s on %s" % (name,ports)) 
   c = client.containers.run('bedrock',
                             name=name,                             
                             ports=ports,
                             mounts=mounts,
                             restart_policy={'Name' : 'on-failure'},
                             detach=True,
                             environment={'WORLD' : name})

def reboot(name):
    c = container(name)
    port = ports(c)[0]
    stop(name)
    start(name,port)

def containers():
    return client.containers.list()

if __name__== "__main__":
   import argparse

   parser = argparse.ArgumentParser(description='Arguments.')
   parser.add_argument('-w','--world', dest="world", action="store",
                       help='World')
   parser.add_argument('-p','--port', dest="port", action="store",type=int,
                       help='Minecraft port [%d]' % config["port"])
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

   if not args.port:
       args.port = next_port()
       print('Using next available port',args.port)

   if args.list:
       for c in containers():
           prts = ports(c)
           print(c.name,','.join([str(p) for p in prts]))

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
      start(args.world, args.port)

   if args.join:
      world_container = container(args.world)
      if world_container:
         world_container.exec_run(cmd="bash",tty=True,stdin=True,stdout=True,stderr=True)

# sudo docker exec -it bedrock bash
# sudo docker stats bedrock
# sudo attach bedrock
