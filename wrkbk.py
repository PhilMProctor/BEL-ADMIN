#!/usr/bin/env python

from google.appengine.ext import ndb

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
    #Give ability to CREATE Unit details
    
    
    def post(self):
        author = users.get_current_user()
        unit1 = wUnit1(unit_title=self.request.get('unit_title'),
                ftype=self.request.get('ftype'),
                outcome1=self.request.get('outcome1'),
                outcome2=self.request.get('outcome2'),
                outcome3=self.request.get('outcome3'),
                outcome4=self.request.get('outcome4'),
                narrative1=self.request.get('narrative1'),
                narrative2=self.request.get('narrative2'),
                narrative3=self.request.get('narrative3'),
                narrative4=self.request.get('narrative4'),
                narrative5=self.request.get('narrative5'),
                narrative6=self.request.get('narrative6'),
                narrative7=self.request.get('narrative7'),
                narrative8=self.request.get('narrative8'),
                narrative9=self.request.get('narrative9'),
                narrative10=self.request.get('narrative10'),
                author=str(author))

        unit1.put()
        return webapp2.redirect('/adminU')
                
    
    def get(self):
        user = users.get_current_user()
        params = {
            'user': user.nickname()
        }
        self.render_template('au1c.html', params)

class au1v_Handler(BaseHandler):
    #Give ability to VIEW Unit details
    def get(self):
        user = users.get_current_user()
        unitNo = wUnit1.query(wUnit1.ftype == "Template")
        params = {
            'unitNo' : unitNo,
            'user': user.nickname()
        }
        
        self.render_template('au1v.html', params)
        
        
class au1e_Handler(BaseHandler):
    #Give ability to EDIT Unit details
    
    def post(self):
        author = users.get_current_user()

        unit1 = wUnit1(unit_title=self.request.get('unit_title'),
                ftype=self.request.get('ftype'),
                outcome1=self.request.get('outcome1'),
                outcome2=self.request.get('outcome2'),
                outcome3=self.request.get('outcome3'),
                outcome4=self.request.get('outcome4'),
                narrative1=self.request.get('narrative1'),
                narrative2=self.request.get('narrative2'),
                narrative3=self.request.get('narrative3'),
                narrative4=self.request.get('narrative4'),
                narrative5=self.request.get('narrative5'),
                narrative6=self.request.get('narrative6'),
                narrative7=self.request.get('narrative7'),
                narrative8=self.request.get('narrative8'),
                narrative9=self.request.get('narrative9'),
                narrative10=self.request.get('narrative10'),
                author=str(author))

        unit1.put()
        return webapp2.redirect('/adminU')
    
    def get(self):
        user = users.get_current_user()
        unitNo = wUnit1.query(wUnit1.ftype == "Template")

        params = {
            'unitNo' : unitNo,
            'user': user.nickname()
        }
        
        self.render_template('au1e.html', params)

application = webapp2.WSGIApplication([
    ('/au1c', au1c_Handler,),
    ('/au1v', au1v_Handler),
    ('/au1e', au1e_Handler),
], debug=True)
