#!/usr/bin/python3
import re
from functools import partial
import arrow
import os

print("Loading parse_server %s" % arrow.now())
session = {}
player = {}

# Line parsing handling functions
def start_session(time):

    #print("Session started at %s" % time)

    session = {"start" : time}
    
    time = arrow.get(time)
    for xuid,p in player.items():
        if player[xuid]["status"] == "connected":
            #print("Player %s is already connected when sessions start" % player[xuid]['name'])
            player[xuid]["status"] = "unconnected"
            on_time = player[xuid]["time"][0]["on"]
            if on_time.day == time.day:
               off_time = time 
            else:   
               off_time = on_time.ceil('day') 

            #print("Updating date %s on time %s with off time %s" % (on_time.date(),on_time,off_time))
            player[xuid]["time"][0]["off"] = off_time 
            player[xuid]["date"][on_time.date()][0]["off"] = off_time

def connect(time,name,xuid):
   
   time = arrow.get(time)
   #print("%s connnected at %s " % (name,time))

   if not xuid in player:
      player[xuid] = {}
      player[xuid]["time"] = []
      player[xuid]["date"] = {}

   if not time.date() in player[xuid]["date"]:
      player[xuid]["date"][time.date()] = []

   player[xuid]["name"] = name
   player[xuid]["xuid"] = xuid
   player[xuid]["status"] = "connected"
   player[xuid]["time"].insert(0,{"on":time})
   player[xuid]["date"][time.date()].insert(0,{"on":time})

def disconnect(time,name,xuid):
   
   #print("%s disconnnected at %s" % (name,time))

   time = arrow.get(time)

   player[xuid]["xuid"] = xuid
   player[xuid]["name"] = name
   player[xuid]["status"] = "disconnected"
   player[xuid]["time"][0]["off"] = time

   date = time.date()
   if date in player[xuid]["date"]:
      player[xuid]["date"][date][0]["off"] = time
   else:   
      last_day  = time.shift(days=-1)
      last_date = last_day.date()
      if last_date in player[xuid]["date"]:
          player[xuid]["date"][last_date][0]["off"] = last_day.ceil('day')
          player[xuid]["date"][date] = []
          player[xuid]["date"][date].insert(0,{"on":time.floor('day')})
          player[xuid]["date"][date][0]["off"] = time
      
def parse_log(logfile = "server.log"):
    print("Parsing log %s" % logfile)
    with open(logfile) as log:
       for l in log:
           parse_line(l)

def parse_line(l):

    #print("Parsing line %s" % l)

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
            #print("Line match = ",handler,m)
            if callable(handler):
                handler(*match.groups()) # call handling function with match groups
            else:
                field = handler
                session[field] = match.group(1) # assum only 1 match for session fields

def online():
    return [player[id] for id in player.keys() if player[id]["status"]=="connected"]

def by_date(times):
    dates = {t['on'].date() for t in times if 'on' in t}
    return {d : [t for t in times if 'on' in t and t['on'].date()==d] for d in dates}

def filter_by_date(date):
    return {p["xuid"] : p for p in player.values() if date in by_date(p['time'])}

def graph(date=None):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    if date.lower()=="now" or date.lower()=="today":
        date = arrow.now().date()
    if date:
        date = arrow.get(date).date()

    date_player = date and filter_by_date(date).values() or player.values()

    # Y ticks are just spaced player rows
    y_tick   = [(t+1)*10 for t in range(len(date_player))]
    y_labels = [p['name'] for p in date_player]

    x_tick = []

    for idx,p in enumerate(date_player):
        #print("player=",p)
        if date:
            if date in p['date']:
                date_times = p['date'][date]
            else:
                date_times = []
        else:
            date_times = p['time']

        #print(date_times)

        for t in date_times:
            if 'on' not in t:
                print("NO on in player %s for %s" % (p['name'],t))
            if 'off' not in t:
                print("NO off in player %s for %s" % (p['name'],t))

        # X values are start/width pairs timestamp pairs
        x_val = [(t['on'].timestamp ,t['off'].timestamp-t['on'].timestamp) for t in date_times if 'off' in t]

        # Y value for this player are start/width pairs
        y_val = (y_tick[idx]-4,8);

        ax.broken_barh(x_val, y_val, facecolors='tab:blue')

        #print("x_val=",x_val) # save our x on/off values as timestamp ticks
        x_tick.extend([x[0] for x in x_val])      # on values
        x_tick.extend([x[0]+x[1] for x in x_val]) # off values

    x_tick.sort() # sort them so that all on's are before off's

    if x_tick:
        if date:
            x_tick   = [d for d in arrow.Arrow.range('hour', arrow.get(x_tick[0]).shift(hours=-1), arrow.get(x_tick[-1]).shift(hours=+1))]
            x_labels = [h.format("HH") for h in x_tick]
        else:
            x_tick   = [d for d in arrow.Arrow.range('day', arrow.get(x_tick[0]).shift(days=-1), arrow.get(x_tick[-1]).shift(days=+1))]
            x_labels = [d.format("MM:DD") for d in x_tick]

    x_tick = [d.timestamp for d in x_tick]

    #print("x_tick=",x_tick)
    print("x_labels=",x_labels)
    print("y_labels=",y_labels)

    ax.set_xlabel('Time')
    if x_tick:
       ax.set_xlim(x_tick[0], x_tick[-1])
       ax.set_xticks(x_tick[1:-1])
       ax.set_xticklabels(x_labels[1:-1])

    ax.set_ylabel('Players')
    if y_tick:
       ax.set_ylim(y_tick[0]-10, y_tick[-1]+10)
       ax.set_yticks(y_tick)
       ax.set_yticklabels(y_labels)

    if not os.access("static",os.F_OK):
        os.mkdir("static")

    plt.tight_layout()
    plt.savefig("static/graph.png")
    #plt.show()

if __name__== "__main__":
    parse_log()

    print(session)

    for p in player.values():
        print(p)

    for p in online():
        print("%s is online" % p["name"])

    dates = {t['on'].date() for p in player.values() for t in p['time'] if 'time' in p}
    for d in dates:
        played_on_date = filter_by_date(d)
        for p in played_on_date.values():
            print("%s played on %s" % (p["name"],d))

    #graph("2019-07-27")
    graph()
