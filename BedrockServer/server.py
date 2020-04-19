#!/usr/bin/env python

import json
import subprocess
import os
import re
import docker

# Get the docker client API
client = docker.from_env()

config = {"bedrock_port" : 19132,
          "java_port"    : 25565}

def build(mc_type='bedrock'):
   print('Building %s image' % mc_type)

   (image,build_log) = client.images.build(
           path='./'+mc_type,
           tag=mc_type+"_server",
           rm=True
   )

   for l in build_log:
       if 'stream' in l:
           print(l['stream'])

def container(name):
   container = None
   try:
      container = client.containers.get(name)
   except docker.errors.NotFound:
      print("No container named",name)

   return container

def mc_type(container):
    repo = [t.split(':')[0] for t in container.image.tags]
    try:
        return re.match("(.*)_server",repo[0])[1]
    except:
        raise IndexError("Container %s does not have a minecraft server type" % container.name)   

def ports(container):
   return [int(v[0]['HostPort']) for k,v in container.attrs['NetworkSettings']['Ports'].items()]

def next_port(mc_type='bedrock'):

    used_prts = [p for c in containers() for p in ports(c)]
    start = config['bedrock_port'] if mc_type=='bedrock' else config['java_port']
    free_prts = [p for p in range(start,start+10) if p not in used_prts]
    
    try:
        return free_prts[0]    
    except IndexError:
        raise IndexError('No free ports')

def stop(name):
   c = container(name)
   if c:
      print("Stopping",name) 
      c.remove(force=True)

def start(name,port,mc_type='bedrock'):

   mounts = [docker.types.Mount(target='/RoboServer', source=os.getcwd(), type='bind')] 
   mc_port = config['bedrock_port'] if mc_type=='bedrock' else config['java_port']

   ports = {str(mc_port) + '/udp' : port}

   if mc_type!='bedrock':
      ports[str(mc_port) + '/tcp'] = port

   print("Starting %s on %s" % (name,ports)) 
   c = client.containers.run(mc_type+'_server',
                             name=name,                             
                             ports=ports,
                             mounts=mounts,
                             restart_policy={'Name' : 'on-failure'},
                             detach=True,
                             stdin_open=True,
                             tty=True,
                             environment={
                                 'WORLD' : name,
                                 'PORT'  : mc_port,
		                 'JAVA_XMX' : '6G',
		                 'ACCEPT_EULA' : True}
                             )

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

   parser.add_argument('-t','-type', dest='mc_type',action='store',default='bedrock',
                       help='Minecraft server type [bedrock,java]')
   parser.add_argument('-w','--world', dest="world", action="store",
                       help='World')
   parser.add_argument('-p','--port', dest="port", action="store",type=int,
                       help='Minecraft port [%d/%d]' % (config['bedrock_port'],config['java_port']))
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

   if not args.world:
      try:
         args.world = containers()[0].name
         print("Using world",args.world)
      except IndexError:
         raise LookupError("No running worlds, must supply world")

   if args.list:
       for c in containers():
           prts = ports(c)
           mc_t = mc_type(c)
           print('%s, type=%s, ports=(%s)' % (c.name,mc_t,','.join([str(p) for p in prts])))

   if args.stop or args.run:
      stop(args.world)

   if args.build:
      build(args.mc_type)

   if args.run: 
      if not args.port:
         args.port = next_port(args.mc_type)
      start(args.world, args.port, args.mc_type)

   if args.join:
      world_container = container(args.world)
      if world_container:
         world_container.exec_run(cmd="bash",tty=True,stdin=True,stdout=True,stderr=True)

# sudo docker exec -it bedrock bash
# sudo docker stats bedrock
# sudo attach bedrock
