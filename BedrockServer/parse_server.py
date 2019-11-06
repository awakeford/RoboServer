#!/usr/bin/python3
import re
from functools import partial

session = {}
player = {}

# Line parsing handling functions
def start_session(time):
    #print("Session started at %s" % time)
    session = {"start" : time}
    for xuid,p in player.items():
        if player[xuid]["status"] == "connected":
            player[xuid]["status"] = "unconnected"
            player[xuid]["time"][0]["off"] = time

def connect(time,name,xuid):
   #print("%s connnected at %s" % (name,time))
   if not xuid in player:
      player[xuid] = {}
      player[xuid]["time"] = []
   player[xuid]["name"] = name
   player[xuid]["xuid"] = xuid
   player[xuid]["status"] = "connected"
   player[xuid]["time"].insert(0,{"on":time})

def disconnect(time,name,xuid):
   #print("%s disconnnected at %s" % (name,time))
   player[xuid]["xuid"] = xuid
   player[xuid]["name"] = name
   player[xuid]["status"] = "disconnected"
   player[xuid]["time"][0]["off"] = time

def parse_log(logfile = "server.log"):
    with open(logfile) as log:
       for l in log:
           parse_line(l)

def parse_line(l):

    # Dictionary of regex match strings for parsing the log lines,
    # Indexed by either handling function or session field.
    match_str = {
        start_session : re.compile("^\[(.*) .*\] Starting Server"),
        "version"     : re.compile(".* Version (.*)"),
        "session_id"  : re.compile(".* Session ID (.*)"),
        "level"       : re.compile(".* Level Name: (.*)"),
        "mode"        : re.compile(".* Game mode: (.*)"),
        "difficulty"  : re.compile(".* Difficulty: (.*)"),
        "port"        : re.compile(".* IPv4 supported, port:  (.*)"),
        connect       : re.compile("^\[(.*) .*\] Player connected: (.*), xuid: (.*)"),
        disconnect    : re.compile("^\[(.*) .*\] Player disconnected: (.*), xuid: (.*)"),
    }

    match = {}
    for handler,m in match_str.items():
        match = m.search(l)

        if match:
            if callable(handler):
                handler(*match.groups()) # call handling function with match groups
            else:
                field = handler
                session[field] = match.group(1) # assum only 1 match for session fields

def online():
    return [player[id] for id in player.keys() if player[id]["status"]=="connected"]

if __name__== "__main__":
    parse_log()

    print(session)

    for p in player.values():
        print(p)

    on_player = online()
    for p in on_player:
        print("%s is online" % p["name"])
