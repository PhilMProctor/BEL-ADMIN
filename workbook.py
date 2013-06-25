from google.appengine.ext.webapp import template
from google.appengine.ext import db

import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import users

class BaseHandler(webapp2.RequestHandler):
  def render_template(self, filename, **template_args):
        path = os.path.join(os.path.dirname(__file__), 'views', filename)
        self.response.write(template.render(path, template_args))
        
class u1Handler(BaseHandler):
  def get(self):
    user = users.get_current_user()
    if user == None:
        user = "Student"
        self.render_template('u1.html', user = user)
    else:
        self.render_template('u1.html', user = users.get_current_user())
        
application = webapp2.WSGIApplication([
    ('/u1', u1Handler,),
], debug=True)


], debug=True)