import cherrypy
import server_log
import os
import arrow
import jinja2
import util
import shutil
import server

root      = os.path.abspath('./')
templates = os.path.join(root,'templates')
static    = os.path.join(root,'static')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

class Trinity(object):

    def __init__(self):
        self.worlds = World()

    @cherrypy.expose
    def index(self):
        world_names     = os.listdir(os.path.join(root,'worlds'))
        container_names = [c.name for c in server.containers()]
        worlds = {w : server.container(w) if w in container_names else None for w in world_names}
        ports = [', port='+str(server.ports(c)[0]) if c else '' for w,c in worlds.items()]
        types = [', type='+str(server.mc_type(c))  if c else '' for w,c in worlds.items()] 
        template = jinja_env.get_template('home.html')
        return template.render(worlds=worlds,ports=ports,types=types)

    @cherrypy.expose
    def download(self,world):

        world_dir = os.path.join(root,'worlds',world) 
        zip_world  = os.path.abspath(os.path.join("./",world+".zip"))

        if os.path.exists(zip_world):
            os.remove(zip_world)

        shutil.make_archive(world, 'zip', world_dir) 

        upload = cherrypy.lib.static.serve_file(zip_world, 'application/x-download',
                                              'attachment', world+".mcworld")
        os.remove(zip_world)

        return upload

@cherrypy.popargs('world_name')
class World(object):

    def world_dir(self,name):
       return os.path.normpath(os.path.join(root,'worlds',name))

    def parse_log(self,name):
       log = os.path.join(self.world_dir(name),"server.log") 
       server_log.parse(log)

    @cherrypy.expose
    def index(self,world_name):
        self.parse_log(world_name)
        world = server.container(world_name)
        up = world!=None
        port = up and server.ports(world)[0] or None            
        template = jinja_env.get_template('world_home.html')        
        return template.render(world=world_name,server_info=server_log.session.items(),on_players=server_log.online(),up=up,port=port)

    @cherrypy.expose
    def log(self,world_name):
        template = jinja_env.get_template('log.html')
        return template.render(log=open("server.log").read())

    @cherrypy.expose
    def graph(self,world_name,date=None):
        
        if not date:
           date=arrow.now().format("YYYY-MM-DD")

        self.parse_log(world_name)
        server_log.graph(date,os.path.join(static,'graph.png'))

        template = jinja_env.get_template('graph.html')
        return template.render(date=date)

    @cherrypy.expose
    def players(self,world_name):
        util.load(self.world_dir(world_name))
        template = jinja_env.get_template('players.html')
        fields = ['name', 'xuid', 'ignoresPlayerLimit','permission']
        return template.render(fields=fields,status=util.all_dict.values())

    @cherrypy.expose
    def add_player(self,world_name,name,ignoresPlayerLimit,permission):
        print("Adding player",name)
        util.load(self.world_dir(world_name))

        player = {"name":name,"ignoresPlayerLimit":ignoresPlayerLimit,"xuid":""}
        if permission!="default":
           player["permission"] = permission

        util.all_dict[name]=player
        util.write()
        return self.players(world_name)

    @cherrypy.expose
    def remove_player(self,world_name,name):
        print("Removing player",name)
        util.load(self.world_dir(world_name))
        if name in util.all_dict:
           del util.all_dict[name]
        util.write()
        return self.players(world_name)

    @cherrypy.expose
    def files(self,world_name):
        template = jinja_env.get_template('files.html') 
        return template.render(worlds=os.listdir("./worlds/"))

    @cherrypy.expose
    def upload(self,world_name,myFile):

        local_name = os.path.join(self.world_dir(world_name),myFile.filename)
        save = not os.path.exists(local_name)

        size = 0
        if save:
            with open(local_name,"wb") as local_file: 
                while True:
                    data = myFile.file.read(8192)
                    if not data:
                        break
                    size += len(data)
                    local_file.write(data)

            template = jinja_env.get_template('uploaded.html') 
            return template.render(length=size,filename=local_name,filetype=myFile.content_type)
        else:
            return "Local file exists, no file uploaded" 

    @cherrypy.expose
    def download(self,world_name,world):

        world_path = self.world_dir(world_name)
        zip_world  = os.path.abspath(os.path.join("./",world+".zip"))

        if os.path.exists(zip_world):
            os.remove(zip_world)

        shutil.make_archive(world, 'zip', world_path)

        return cherrypy.lib.static.serve_file(zip_world, 'application/x-download',
                                              'attachment', world+".mcworld")

    @cherrypy.expose
    def up(self,world_name):
       return self.server_cmd(world_name,cmd='start')

    @cherrypy.expose
    def down(self,world_name):
       return self.server_cmd(world_name,cmd='stop')

    @cherrypy.expose
    def reboot(self,world_name):
       return self.server_cmd(world_name,cmd='reboot')

    def server_cmd(self,world_name,cmd):
    
        if cmd not in ['start','stop','reboot']:
           raise cherrypy.HTTPError(404)

        world  = server.container(world_name)
        if world and cmd=='reboot':
           port = server.ports(world)[0]
        else:
           port = server.next_port() 

        if cmd=='stop' or cmd=='reboot':
           server.stop(world_name)
        if cmd=='reboot' or cmd=='start':
           server.start(world_name,port)

        return self.index(world_name) 


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 80

conf = {
    '/': {
        'tools.staticdir.debug': True,
        'log.screen': True,
        'tools.sessions.on': True,
        'tools.staticdir.root': static,
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': ''
    }
}

def start():
    cherrypy.quickstart(Trinity(),'/',conf)

if __name__== "__main__":
    start()
