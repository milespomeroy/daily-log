import os # for file path stuff
from google.appengine.ext.webapp import template # html templating
from google.appengine.api import users # google user authentication
from google.appengine.ext import webapp # webapp framework
from google.appengine.ext.webapp.util import run_wsgi_app # wsgi datetime

import datetime # for date stuff

class PstTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(hours=-8)
  def dst(self, dt): return datetime.timedelta(0)


class MainHandler(webapp.RequestHandler):

	def get(self):
		user = users.get_current_user() # get user
		if user:
			pst = PstTzinfo()
			today = datetime.datetime.now(pst)
			thedate = today.strftime("%A, %B %e, %Y")
			
			# path of html file
			path = os.path.join(os.path.dirname(__file__), 'index.html')
			values = {
				'user': user,
				'today': today,
				'date': thedate,
			}
			self.response.out.write(template.render(path, values))
		else: # not logged in
			self.redirect(users.create_login_url(self.request.uri))


def main():
	application = webapp.WSGIApplication([('/', MainHandler)], 
		debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()
