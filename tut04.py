import random 
import string

import cherrypy

class StringGenerator(object):
	@cherrypy.expose
	#exposed handler 
	def index(self):
		return """<html>
		<head></head>
		<body>
			<form method ="post" action="generate">
			 	<input type="text" value="8" name="length" />
				<button type="submit">Give it now!</button>
			</form>
		</body>
	</html>"""

	@cherrypy.expose
	#exposed handler, functions defined with def
	def generate(self, length=8):
		return ''.join(random.sample(string.hexdigits,int(length)))

if __name__ =='__main__':
	cherrypy.quickstart(StringGenerator())
