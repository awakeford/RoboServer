import cherrypy
import parse_server

class Trinity(object):

    def server_status(self):
        str = "<h1>Trinity Server is up!</h1>"
        parse_server.parse_log();

        for k,v in parse_server.session.items():
            str += "<p>%s = %s</p>" % (k,v)

        on_players = parse_server.online()
        if not players:
            str += "<p>No players are online at the moment!</p>"
        for p in on_players:
            str += "<p>%s is online</p>" % p["name"]
        return str

    @cherrypy.expose
    def log(self):
        str = ""
        with open("server.log") as log:
            for l in log:
                str += "<p>%s</p>" % l
        return str

    @cherrypy.expose
    def index(self):
        return self.server_status()

    @cherrypy.expose
    def graph(self,date=None):
        parse_server.parse_log()
        parse_server.graph(date)

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 80

cherrypy.quickstart(Trinity())
