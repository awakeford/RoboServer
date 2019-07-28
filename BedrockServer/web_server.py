import cherrypy
import parse_server

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return server_status()

    def server_status():
        parse_server.parse_log();
        str = "Trinity Server is up!\n"
        print("\n")
        for k,v in parse_server.session.items():
            str += "%s = %s\n" % (k,v)
        str += "\n"

        on_players = parse_server.online()
        for p in on_players:
            str += "%s is online\n" % p["name"]
        return str

#print(HelloWorld.server_status())
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 80

cherrypy.quickstart(HelloWorld())
