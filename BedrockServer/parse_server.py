#!/usr/bin/python3


#[2019-07-27 15:18:11 INFO] Starting Server
#[2019-07-27 15:18:11 INFO] Version 1.12.0.28
#[2019-07-27 15:18:11 INFO] Session ID 568ca736-c53f-4630-82d6-10fbc1bd030e
#[2019-07-27 15:18:11 INFO] Level Name: Trinity_Server
#[2019-07-27 15:18:11 INFO] Game mode: 0 Survival
#[2019-07-27 15:18:11 INFO] Difficulty: 2 NORMAL
#[2019-07-27 15:18:13 INFO] IPv4 supported, port: 19132
#[2019-07-27 15:18:13 INFO] IPv4 supported, port: 57775
#[2019-07-27 15:18:15 INFO] Server started.
#[2019-07-27 16:05:08 INFO] Player connected: RoboLegoPlayer, xuid: 2535440106087
#[2019-07-27 17:24:58 INFO] Player disconnected: RoboLegoPlayer, xuid: 2535440106

with open("server.log") as log:
   for l in log:
      print(l)