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
    narrative1 = nndb.TextProperty()
    narrative2 = nndb.TextProperty()
    narrative3 = nndb.TextProperty()
    narrative4 = nndb.TextProperty()
    narrative5 = nndb.TextProperty()
    narrative6 = nndb.TextProperty()
    narrative7 = nndb.TextProperty()
    narrative8 = nndb.TextProperty()
    narrative9 = nndb.TextProperty()
    narrative10 = nndb.TextProperty()
    author = nndb.StringProperty()
    ftype = nndb.StringProperty(required=False, choices=set(["Template", "Page"]))
    date = nndb.DateTimeProperty(auto_now_add=True)


class Students(nndb.Model):

    username = nndb.StringProperty()
    password = nndb.StringProperty()
    courseN = nndb.StringProperty()
    courseT = nndb.StringProperty()
    
class Tutors (nndb.Model):

    username = nndb.StringProperty()
    password = nndb.StringProperty()
    role = nndb.StringProperty()