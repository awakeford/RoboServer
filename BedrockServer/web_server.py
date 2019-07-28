import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Trinity Server is up!"

cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 80

cherrypy.quickstart(HelloWorld())
