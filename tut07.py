import random
import string

import cherrypy
import json


class ValidateUser(object):
 exposed = True


#need to create threads for handling multiple requests? 

 @cherrypy.tools.accept(media='text/JSON')
 def GET(self):
     #return cherrypy.session['mystring']
     user = {
            'username':"faircoder",
            'password':"servethepi123"

     }
     #return mock JSON
     return json.dumps(user)

 def POST(self, length=8):
     some_string = ''.join(random.sample(string.hexdigits, int(length)))
     cherrypy.session['mystring'] = some_string
     return some_string

 def PUT(self, another_string):
     cherrypy.session['mystring'] = another_string

 def DELETE(self):
     cherrypy.session.pop('mystring', None)

if __name__ == '__main__':
 conf = {
     '/': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.sessions.on': True,
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'text/JSON')],
     }
 }
 #cherrypy.config.update({'server.socket_port':8080,})  
 cherrypy.quickstart(ValidateUser(), '/', conf)