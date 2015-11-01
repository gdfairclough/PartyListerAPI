import random
import string

import cherrypy




class ValidateUser(object):
 exposed = True


    
#need to create threads for handling multiple requests? 

 @cherrypy.tools.accept(media='text/plain')
 def GET(self):
     #return cherrypy.session['mystring']

     #return mock JSON
     return '{"NEW_ACC": {"USERNAME": "Stone123", "PASSWORD": "123","EMAIL": "user_email"}}'

 def POST(self, length=8):
     # some_string = ''.join(random.sample(string.hexdigits, int(length)))
     # cherrypy.session['mystring'] = some_string
     # return some_string

 def PUT(self, another_string):
     # cherrypy.session['mystring'] = another_string

 def DELETE(self):
     # cherrypy.session.pop('mystring', None)



class Event(object):
 exposed = True

 @cherrypy.tools.accept(media="text/plain")
 def GET(self):

 def POST(self):
    #insert an event into the db 

if __name__ == '__main__':
 conf = {
     '/': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.sessions.on': True,
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'text/plain')],
     }
 }
 cherrypy.config.update({'server.socket_port':8080,})  
 cherrypy.quickstart(ValidateUser(), '/user', conf)
 cherrypy.quickstart(Event(),'/event',conf)
 