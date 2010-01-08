import os # for file path stuff
from google.appengine.ext.webapp import template # html templating
from google.appengine.api import users # google user authentication
from google.appengine.ext import webapp # webapp framework
from google.appengine.ext.webapp.util import run_wsgi_app # wsgi datetime
from google.appengine.ext import db # db stuff
from datetime import tzinfo, timedelta, datetime, date # for date stuff


class MainHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user() # get user
		if user:
			today = datetime.now(PstTzinfo())
			theDate = today.strftime("%A, %B %e, %Y")
			query = db.GqlQuery("""SELECT * FROM JrEntry 
				WHERE date = :1""", today.date())
			result = query.get()
			
			# path of html file
			path = os.path.join(os.path.dirname(__file__), 'index.html')
			values = {
				'user': user,
				'date': theDate,
				'year': today.year,
				'month': today.month,
				'day': today.day,
				'content': '',
				'logout': users.create_logout_url(self.request.uri)
			}
			
			if result:
				values['content'] = result.content
			
			self.response.out.write(template.render(path, values))
			
		else: # not logged in
			self.redirect(users.create_login_url(self.request.uri))


class PostIt(webapp.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if user:
			entry = JrEntry()
			
			year = int(self.request.get('year'))
			month = int(self.request.get('month'))
			day = int(self.request.get('day'))
			
			entry.author = user
			entry.content = self.request.get('content')
			entry.date = date(year, month, day)
			
			entry.put()
					
		else: # not logged in
			self.redirect(users.create_login_url(self.request.uri))
			

class JrEntry(db.Model):
	author = db.UserProperty()
	content = db.TextProperty()
	date = db.DateProperty()


# tzinfo class for Pacific Standard Time, from timezones.appspot.com
class PstTzinfo(tzinfo):
	def utcoffset(self, dt): 
		return timedelta(hours=-8)
	def dst(self, dt): 
		return timedelta(0)
	def tzname(self, dt): 
		return 'PST+08PDT'


def main():
	application = webapp.WSGIApplication([('/', MainHandler),
		('/post', PostIt)], 
		debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()
