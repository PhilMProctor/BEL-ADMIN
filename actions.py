import webapp2
import os
from models import Students
from google.appengine.ext import db

class CreateUser(webapp2.RequestHandler):
    def post(self):
        s = Students (name=self.request.get('name'),
                        email=self.request.get('email'),
                        username=self.request.get('username'),
                        password=self.request.get('password'),
                        courseN=self.request.get('courseN'),
                        courseT=sef.request.get('courseT'))
        s.put()
    
