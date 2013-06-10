from google.appengine.ext import db


class Students(db.Model):

    name = db.StringProperty()
    email = db.StringProperty() 
    username = db.StringProperty()
    password = db.StringProperty()
    courseN = db.StringProperty()
    courseT = db.StringProperty()
    
class Tutors (db.Model):

    name = db.StringProperty()
    email = db.StringProperty() 
    username = db.StringProperty()
    password = db.StringProperty()
    role = db.StringProperty()
