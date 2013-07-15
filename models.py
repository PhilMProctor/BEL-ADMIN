from google.appengine.ext import db
from webapp2_extras import sessions
from webapp2_extras import auth

import logging
import os.path
import webapp2

class wUnit1(db.Model):
    #Workbook Unit 1 Datastore
    unit_title = db.StringProperty()
    unit_no = db.StringProperty()
    outcome1 = db.StringProperty()
    outcome2 = db.StringProperty()
    outcome3 = db.StringProperty()
    outcome4 = db.StringProperty()
    narrative1 = db.TextProperty()
    narrative2 = db.TextProperty()
    narrative3 = db.TextProperty()
    narrative4 = db.TextProperty()
    narrative5 = db.TextProperty()
    narrative6 = db.TextProperty()
    narrative7 = db.TextProperty()
    narrative8 = db.TextProperty()
    narrative9 = db.TextProperty()
    narrative10 = db.TextProperty()
    author = db.StringProperty()
    ftype = db.StringProperty(required=False, choices=set(["Template", "Page"]))
    date = db.DateTimeProperty(auto_now_add=True)


class Students(db.Model):

    username = db.StringProperty()
    password = db.StringProperty()
    courseN = db.StringProperty()
    courseT = db.StringProperty()
    
class Tutors (db.Model):

    username = db.StringProperty()
    password = db.StringProperty()
    role = db.StringProperty()