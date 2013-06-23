#from google.appengine.ext import db

from google.appengine.ext import db

class Students(db.Model):

    username = db.StringProperty()
    password = db.StringProperty()
    courseN = db.StringProperty()
    courseT = db.StringProperty()
    
class Tutors (db.Model):

    username = db.StringProperty()
    password = db.StringProperty()
    role = db.StringProperty()