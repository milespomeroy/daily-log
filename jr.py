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
			# date info
			today = datetime.now(PstTzinfo())
			theDate = today.strftime("%A, %B %e, %Y")
			
			# get entry if it exists
			gquery = db.GqlQuery("""SELECT * FROM JrEntry 
				WHERE date = :1 AND author = :2""", 
				today.date(), user)
			result = gquery.get()
			
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
			
			# if there is an entry, set content to it
			if result:
				values['content'] = result.content
			
			self.response.out.write(template.render(path, values))
			
		else: # not logged in
			self.redirect(users.create_login_url(self.request.uri))
			
	
class PostEntry(webapp.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if user:
			# date info
			year = int(self.request.get('year'))
			month = int(self.request.get('month'))
			day = int(self.request.get('day'))
			
			# get entry if for date if exists
			pquery = db.GqlQuery("""SELECT * FROM JrEntry 
				WHERE date = :1 AND author = :2""", 
				date(year, month, day), user)
			entry = pquery.get()
			
			# if entry doesn't exist, create it
			if not entry:
				entry = JrEntry()
				entry.author = user
				entry.date = date(year, month, day)
			
			# get content for entry
			entry.content = self.request.get('content')
						
			entry.put() # put into datastore
			#self.redirect('/')
					
		else: # not logged in
			self.redirect(users.create_login_url(self.request.uri))
			
			
class AboutHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user() # get user
		if user:
			# path of html file
			path = os.path.join(os.path.dirname(__file__), 'about.html')
			values = {
				'user': user,
				'logout': users.create_logout_url(self.request.uri)
			}
			
			self.response.out.write(template.render(path, values))
			
		else: # not logged in
			self.redirect(users.create_login_url(self.request.uri))


class GetHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			# date info
			year = int(self.request.get('year'))
			month = int(self.request.get('month'))
			day = int(self.request.get('day'))
		
			# get entry if for date if exists
			query = db.GqlQuery("""SELECT * FROM JrEntry 
				WHERE date = :1 AND author = :2""", 
				date(year, month, day), user)
			entry = query.get()
			
			if entry:
				self.response.out.write(entry.content)


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
		('/post', PostEntry), ('/get', GetHandler), 
		('/about', AboutHandler)], 
		debug=True)
	run_wsgi_app(application)


if __name__ == '__main__':
	main()
