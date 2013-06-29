from google.appengine.ext import db

import jinja2
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

#Addition
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'views')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class BaseHandler(webapp2.RequestHandler):
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)
        
    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))

class MainPage(BaseHandler):
  def get(self):
    user = users.get_current_user()
    if user == None:
        user = "Student"
        self.render_template('home.html', {'user' : user})
    else:
        self.render_template('home.html', {'user' : users.get_current_user()})
            
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
    
interest = "interesting"
 
class Admin(BaseHandler):
    #Main Admin portal page
    def get(self):
        user = users.get_current_user()
        params = {
            'user': user,
            'interest': interest
        }
        self.render_template('admin.html', params)


class LoginHandler(BaseHandler):
# Handles user login requests

    def get(self):
        user = users.get_current_user()
        if user:
            return self.render_template('portal.html', {'user' : users.get_current_user()})
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url(self.request.uri))
        self.response.out.write(WELCOME % greeting)
        #self.render_template('signin.html', greeting = greeting)
        
class LogoutHandler(BaseHandler):
    #Handles user logout requests
    
    def get(self):
        return webapp2.redirect(users.create_logout_url("/"))
        
class adminU_Handler(BaseHandler):

    def get(self):
        user = users.get_current_user()
        self.render_template('adminU.html', {'user':user})  

application = webapp2.WSGIApplication([
    ('/', MainPage,),
    ('/admin', Admin ),
    ('/adminU', adminU_Handler),
    ('/portal', LoginHandler),
    ('/signin', LoginHandler),
    ('/logout', LogoutHandler),
], debug=True)

logging.getLogger().setLevel(logging.DEBUG)