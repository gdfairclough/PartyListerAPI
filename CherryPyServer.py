import random
import string
import json
import pymysql
from datetime import datetime
import time
import logging 

import cherrypy

#receive requests sent to dalepi.duckdns.org:85/user
class ValidateUser(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')

    def GET(self):

        #return mock JSON
        return '{"NEW_ACC": {"USERNAME": "Stone123", "PASSWORD": "123","EMAIL": "user_email"}}'

    def POST(self, length=8):
         some_string = ''.join(random.sample(string.hexdigits, int(length)))
         cherrypy.session['mystring'] = some_string
         return some_string

    def PUT(self, another_string):
         cherrypy.session['mystring'] = another_string

    def DELETE(self):
         cherrypy.session.pop('mystring', None)


#receive requests sent to dalepi.duckdns.org:85/event
class Event(object):
    exposed = True
    @cherrypy.tools.accept(media="text/plain")
    def GET(self):
        #return JSON Event Object 
        return '{"NEW_ACC": {"USERNAME": "Stone123", "PASSWORD": "123","EMAIL": "user_email"}}'
        #return '{"EVENT_INFO": {"NAME": "event_name","DATE": "event_date","LOCATION": "event_location","INVITEES": ["invitee_1","invitee_2","invitee_N"],"ITEMS_LIST": [{"ITEM": {"NAME": "name","DESCRIPTION": "description","QUANTITY": 0,"TOTAL_COST": 0,"DELEGATE": "delegate","ACQUIRED": 0,"REMAINING": 0}}]}}'
    def POST(self, event_json):
        #insert an event into the db and return a value of SUCCESS or FAILURE
        return add_event(event_json)

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
 cherrypy.tree.mount(ValidateUser(), '/user', conf)
 cherrypy.tree.mount(Event(),'/event',conf)
 #configure_logging()

 def configure_logging():
    logging.basicConfig(filename='cherrypy.log',level=logging.DEBUG)
    return

 #pull values from event json
 def add_event(event_json):
    date_format = "%m/%d/%Y, %H:%M:%S"

    eventDict = json.loads(event_json)
    eventInfo = eventDict.get("EVENT_INFO")
    eventId = eventInfo.get("ID")
    name = eventInfo.get("NAME")
    date = eventInfo.get("DATE")
    date = datetime.strptime(date, date_format)
    start = datetime.strptime(eventInfo.get("START"), date_format)
    end = datetime.strptime(eventInfo.get("END"), date_format)
    location = eventInfo.get("LOCATION")
    description = eventInfo.get("DESC")

    #event_string = "Name: %s, Date: %s, Start %s, End: %s, Location: %s, Description: %s"%(name,date,start,end,location,description)

    acknowledge = 'SUCCESS'
    try:
        conn = getDatabaseConnection()
        cur = conn.cursor()
        #insert or update depending on if the event id is already in the database
        if eventId == -1:
            cur.execute('INSERT INTO Event (Event_name, Location, Date, Start_time, End_Time, Event_des)'+
            ' VALUES("%s","%s","%s","%s","%s","%s")'%(name,location,date,start,end,description))
            #get the id of the event that was just inserted 
            cur.execute('SELECT MAX(Event_Id) FROM Event')
            newId = cur.fetchone
            print(newId)
        else:
            print('update Event SET Event_name = \'%s\', Location = \'%s\', Date = "%s", Start_time = "%s", End_Time = "%s", Event_des=\'%s\' WHERE Event_Id = %s'%(name,location,date,start,end,description,eventId))
            cur.execute('update Event SET Event_name = \'%s\', Location = \'%s\', Date = "%s", Start_time = "%s", End_Time = "%s", Event_des=\'%s\' WHERE Event_Id = %s'%(name,location,date,start,end,description,eventId))
            

        conn.commit()
        cur.close()
        conn.close()
    except pymysql.Error as e:
        print("MySQL Error %d: %s" % (e.args[0], e.args[1]))
        #log the error to the log file 
        error_msg = "MySQL Error %d: %s" % (e.args[0], e.args[1])
        logging.error(error_msg)

        logging.basicConfig(filename='cherrypy.log',level=logging.DEBUG)
        acknowledge = 'FAILURE'

    return acknowledge

 def getDatabaseConnection():
    return pymysql.connect(host='localhost', user='pi',passwd='piaccess12!',db='party_time',port=3306)


 
 cherrypy.engine.start()
 cherrypy.engine.block()
 