#!/usr/bin/env python

from google.appengine.ext import db

import jinja2
import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from models import wUnit1

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import users

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'views')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

class BaseHandler(webapp2.RequestHandler):
    #Test for jinja2 templates
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
        
    def user(self):
        user = users.get_current_user()
        return user
    
        
class au1c_Handler(BaseHandler):
    #Give ability to create Unit details
    
    
    def post(self):
        author = users.get_current_user()
        unit1 = wUnit1(unit_title=self.request.get('unit_title'),
                objective1=self.request.get('objective1'),
                objective2=self.request.get('objective2'),
                objective3=self.request.get('objective3'),
                objective4=self.request.get('objective4'),
                narrative1=self.request.get('narrative1'),
                narrative2=self.request.get('narrative2'),
                narrative3=self.request.get('narrative3'),
                narrative4=self.request.get('narrative4'),
                author=str(author))

        unit1.put()
        return webapp2.redirect('/adminU')
                
    
    def get(self):
        user = users.nickname()
        self.render_template('au1c.html', {'user':user})

class au1v_Handler(BaseHandler):
    #Give ability to view Unit details
    def get(self):
        unitNo = wUnit1.all()
        
        self.render_template('au1v.html', {'unitNo' : unitNo})
        
application = webapp2.WSGIApplication([
    ('/au1c', au1c_Handler,),
    ('/au1v', au1v_Handler),
], debug=True)
