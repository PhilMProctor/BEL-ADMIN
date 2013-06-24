from google.appengine.ext.webapp import template
from google.appengine.ext import db

import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from models import Students
from pages import WELCOME, sADMIN_PAGE_HTML
from google.appengine.api import users

class BaseHandler(webapp2.RequestHandler):
  def render_template(self, filename, **template_args):
        path = os.path.join(os.path.dirname(__file__), 'views', filename)
        self.response.write(template.render(path, template_args))

class MainPage(BaseHandler):
  def get(self):
    user = users.get_current_user()
    if user == None:
        user = "Student"
        self.render_template('home.html', user = user)
    else:
        self.render_template('home.html', user = users.get_current_user())
            
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

class LoginHandler(BaseHandler):
# Handles user login requests

    def get(self):
        user = users.get_current_user()
        if user:
            return self.render_template('portal.html', user = users.get_current_user())
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
        self.response.out.write(WELCOME % greeting)
        #self.render_template('signin.html', greeting = greeting)
        
class LogoutHandler(BaseHandler):
    #Handles user logout requests
    
    def get(self):
        return webapp2.redirect(users.create_logout_url("/"))
        
    

application = webapp2.WSGIApplication([
    ('/', MainPage,),
    ('/admin', sAdmin ),
    ('/portal', LoginHandler),
    ('/signin', LoginHandler),
    ('/logout', LogoutHandler),
], debug=True)

logging.getLogger().setLevel(logging.DEBUG)