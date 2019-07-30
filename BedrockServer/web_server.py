import cherrypy
import parse_server

class HelloWorld(object):

    def server_status(self):
        parse_server.parse_log();
        str = "<h1>Trinity Server is up!</h1>"
        str += "<br/>"
        for k,v in parse_server.session.items():
            str += "<p> %s = %s</p>" % (k,v)
        str += "<br/>"

        on_players = parse_server.online()
        for p in on_players:
            str += "<p>%s is online</p>" % p["name"]
        str += "<br/>"
        return str

    @cherrypy.expose
    def index(self):
        return self.server_status()

#print(HelloWorld.server_status())
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 80

cherrypy.quickstart(HelloWorld())
