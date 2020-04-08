#!/usr/bin/python3

import json
import os

world_dir = './'

all_dict = {}

installed_resource_packs = {}
installed_behavior_packs = {}

# Need to be ordered
resource_packs = []
behavior_packs = []

def add_values(vals):

    global all_dict

    for v in vals:
        if "name" in v:
           if not v["name"] in all_dict:
              all_dict[v["name"]] = {}
           all_dict[v["name"]].update(v)
        elif "xuid" in v:
           for name,d in all_dict.items():
              if "xuid" in d and d["xuid"] == v["xuid"]:
                 d.update(v)

def load(dir = world_dir):

   global resource_packs, installed_resource_packs
   global behavior_packs, installed_behavior_packs

   with open(os.path.join(dir,"whitelist.json"), "r") as wf:
      whitelist = json.load(wf)

   with open(os.path.join(dir,"permissions.json"), "r") as pf:
      permissions = json.load(pf)

   add_values(whitelist)
   add_values(permissions)

   for  p in installed_packs(dir,resource=True):
      installed_resource_packs[p['header']['uuid']] = p
   print('installed_resource_packs',installed_resource_packs)

   for  p in installed_packs(dir,resource=False):
      installed_behavior_packs[p['header']['uuid']] = p

   pack_file = os.path.join(dir,"world_resource_packs.json")
   print('loading',pack_file)
   if os.path.exists(pack_file):
      with open(pack_file, "r") as rp:
         print('loading packs') 
         resource_packs = [installed_resource_packs[p['pack_id']] for p in json.load(rp) if p and 'pack_id' in p] 
 
   pack_file = os.path.join(dir,"world_behavior_packs.json")
   if os.path.exists(pack_file):
      with open(pack_file, "r") as bp:
         behavior_packs = [installed_behavior_packs[p['pack_id']] for p in json.load(bp) if p and 'pack_id' in p]

def write(dir=world_dir):

   whitelist = [] 
   permissions = []

   for name, d in all_dict.items():
      if not "banned" in d or not d["banned"]:
         whitelist.append({"name"               : d["name"],
                           "xuid"               : d["xuid"],
                           "ignoresPlayerLimit" : d["ignoresPlayerLimit"]})

      if "permission" in d and d["permission"]!="member":
         permissions.append({"xuid"             : d["xuid"],
                             "permission"       : d["permission"]})
                                  
   with open(os.path.join(dir,"whitelist.json"),"w") as wf:
      json.dump(whitelist,wf,indent=4)

   with open(os.path.join(dir,"permissions.json"),"w") as pf:
      json.dump(permissions,pf,indent=4)

   with open(os.path.join(dir,"world_resource_packs.json"),"w") as rp:
       pack_data = [{'pack_id' : r['header']['uuid'],
                     'version' : r['header']['version']} for r in resource_packs]
       json.dump(pack_data,rp,indent=4)

   with open(os.path.join(dir,"world_behavior_packs.json"),"w") as bp:
       pack_data = [{'pack_id' : b['header']['uuid'],
                     'version' : b['header']['version']} for b in behavior_packs]
       json.dump(pack_data,bp,indent=4)

def get_pack(dir,name,resource):
     pack_dir = 'resource_packs' if resource else 'behavior_packs'
     
     manifest = os.path.join(dir,pack_dir,name,'manifest.json')
     with open(manifest,'r') as mf:
         return json.load(mf)

def installed_packs(dir,resource):

     pack_dir = 'resource_packs' if resource else 'behavior_packs'
     pack_dir = os.path.join(dir,pack_dir)

     if os.path.exists(pack_dir):
        pack_names = [os.path.basename(d) for d in os.listdir(pack_dir)]
     else:
        pack_names = []

     return [get_pack(dir,n,resource) for n in pack_names]

if __name__== "__main__":
   import argparse

   parser = argparse.ArgumentParser(description='Arguments.')

   parser.add_argument('-l','-list', dest="list", action="store_true",
                       help='List players')
   parser.add_argument('-n','--name', dest="name", action="store",
                       help='Player name')
   parser.add_argument('-s','--show', dest="show", action="store_true",
                       help='Show player')
   parser.add_argument('-a','--add', dest="add", action="store_true",
                       help='Add a player (un-ban')
   parser.add_argument('-b','--ban', dest="ban", action="store_true",
                       help='Ban a player')

   parser.add_argument('-u','--xuid', dest="xuid", action="store", default="",
                       help='Player xuid')

   parser.add_argument('-i','--ignoresPlayerLimit', dest='ignoresPlayerLimit', action="store_true",
                       help='Player ignores player limit')

   parser.add_argument('-p','--permission', dest="permission", action="store", default="member",
                       help='Player permission')

   args = parser.parse_args()

   load()

   if args.list:
      for name in all_dict:
         print(name)

   if args.name:

       if args.name in all_dict:
          player = all_dict[args.name]

          if args.ban:
               del all_dict[args.name]

       elif args.add:
          player = {"name"               : args.name,
                    "ignoresPlayerLimit" : args.ignoresPlayerLimit,
                    "xuid"               : args.xuid,
                    "permission"         : args.permission}
          
          all_dict[args.name] = player

       if args.show:
           print(player)
    
   write()
