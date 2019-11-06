import cherrypy
import parse_server

class Trinity(object):

    def server_status(self):
        parse_server.parse_log();
        str = "<h1>Trinity Server is up!</h1>"
        str += "<br/>"
        for k,v in parse_server.session.items():
            str += "<p> %s = %s</p>" % (k,v)
        str += "<br/>"

        on_players = parse_server.online()

        if not on_players:
            str += "<p> No players online</p>"

        for p in on_players:
            str += "<p>%s is online</p>" % p["name"]
        str += "<br/>"
        return str

    @cherrypy.expose
    def index(self):
        return self.server_status()

    @cherrypy.expose
    def log(self):
        str = "<h1>Trinity Server Log</h1>"
        with open("server.log") as logfile:
            for line in logfile:
                str += "<p>%s</p>" % line
        return str

#print(HelloWorld.server_status())
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 80

cherrypy.quickstart(Trinity())
