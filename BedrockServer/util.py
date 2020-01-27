#!/usr/bin/python3

import json

all_dict = {}

def add_values(vals):
    for v in vals:
        if "name" in v:
           if not v["name"] in all_dict:
              all_dict[v["name"]] = {}
           all_dict[v["name"]].update(v)
        elif "xuid" in v:
           for name,d in all_dict.items():
              if "xuid" in d and d["xuid"] == v["xuid"]:
                 d.update(v)

def load():

   with open("whitelist.json", "r") as wf:
      whitelist = json.load(wf)

   with open("permissions.json", "r") as pf:
      permissions = json.load(pf)

   add_values(whitelist)
   add_values(permissions)


def write():

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
                                  
   with open("whitelist.json","w") as wf:
      json.dump(whitelist,wf,indent=4)

   with open("permissions.json","w") as pf:
      json.dump(permissions,pf,indent=4)

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
