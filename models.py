from google.appengine.ext import ndb
from webapp2_extras import sessions
from webapp2_extras import auth

import logging
import os.path
import webapp2

class wUnit1(ndb.Model):
    #Workbook Unit 1 Datastore
    unit_title = ndb.StringProperty()
    unit_no = ndb.StringProperty()
    outcome1 = ndb.StringProperty()
    outcome2 = ndb.StringProperty()
    outcome3 = ndb.StringProperty()
    outcome4 = ndb.StringProperty()
    narrative1 = ndb.TextProperty()
    narrative2 = ndb.TextProperty()
    narrative3 = ndb.TextProperty()
    narrative4 = ndb.TextProperty()
    narrative5 = ndb.TextProperty()
    narrative6 = ndb.TextProperty()
    narrative7 = ndb.TextProperty()
    narrative8 = ndb.TextProperty()
    narrative9 = ndb.TextProperty()
    narrative10 = ndb.TextProperty()
    author = ndb.StringProperty()
    ftype = ndb.StringProperty(required=False, choices=set(["Template", "Page"]))
    date = ndb.DateTimeProperty(auto_now_add=True)


class Students(ndb.Model):

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    courseN = ndb.StringProperty()
    courseT = ndb.StringProperty()
    
class Tutors (ndb.Model):

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    role = ndb.StringProperty()
