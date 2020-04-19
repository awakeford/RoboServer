#!/usr/bin/env python

import json

if __name__== "__main__":
   import argparse

   parser = argparse.ArgumentParser(description='Arguments.')

   parser.add_argument('-f','-file', dest='json_file',action='store',default='whitelist.json',
                       help='JSON file')

   args = parser.parse_args()

   with open(args.json_file, "r") as rf:
      val = json.load(rf)

   with open(args.json_file, "w") as wf:
      json.dump(val,wf,indent=4)

