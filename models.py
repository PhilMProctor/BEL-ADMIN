from google.appengine.ext import ndb


class Students(ndb.Model):

    name = ndb.StringProperty()
    email = ndb.StringProperty() 
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    courseN = ndb.StringProperty()
    courseT = ndb.StringProperty()
    
class Tutors (ndb.Model):

    name = ndb.StringProperty()
    email = ndb.StringProperty() 
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    role = ndb.StringProperty()
