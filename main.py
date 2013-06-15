import webapp2
import cgi
from models import Students
from pages import LOGIN_PAGE_HTML, sADMIN_PAGE_HTML
from google.appengine.api import users


class MainPage(webapp2.RequestHandler):
# Loads the home page

    def get(webapp2):
        webapp2.redirect('h/home.html')
        
class sAdmin(webapp2.RequestHandler):
# Adds entries in Students Entity within the Datastore

    def get(self):
                self.response.write(sADMIN_PAGE_HTML)
    
    def post(self):
        s = Students (  username=self.request.get('username'),
                        password=self.request.get('password'),
                        courseN=self.request.get('courseN'),
                        courseT=self.request.get('courseT'))
        s.put()
        return webapp2.redirect('/')

class sLogin(webapp2.RequestHandler):
    #launches login modal

    def get(self):
    
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">Continue</a>)' %
                        (user.nickname(), webapp2.redirect('/p/portal')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write(LOGIN_PAGE_HTML % greeting)
        

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', sAdmin),
    ('/student', sLogin),
], debug=True)