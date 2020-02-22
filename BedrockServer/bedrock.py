#!/usr/bin/python3

import subprocess
import threading
import web_server

bedrock = None
web = None

def start_web_server():
    global web

    if web and web.is_alive():
       pass 
    else:
       web = threading.Thread(target=web_server.start)
       web.start()

def start_bedrock():
    global bedrock
    if bedrock:
        stop_bedrock()

    server_log = open("server2.log","a")
    bedrock = subprocess.Popen("bedrock_server",env={"LD_LIBRARY_PATH":"."},stdin=subprocess.PIPE,stdout=server_log)

def stop_bedrock():
    bedrock.terminate()
    bedrock.wait()
    server_log.close()

if __name__== "__main__":
    start_web_server()
    start_bedrock()
