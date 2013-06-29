from google.appengine.ext import db

class wUnit1(db.Model):
    #Workbook Unit 1 Datastore
    unit_title = db.StringProperty()
    unit_no = db.StringProperty()
    objective1 = db.StringProperty()
    objective2 = db.StringProperty()
    objective3 = db.StringProperty()
    objective4 = db.StringProperty()
    objective5 = db.StringProperty()
    narrative1 = db.StringProperty()
    narrative2 = db.StringProperty()
    narrative3 = db.StringProperty()
    narrative4 = db.StringProperty()

class Students(db.Model):

    username = db.StringProperty()
    password = db.StringProperty()
    courseN = db.StringProperty()
    courseT = db.StringProperty()
    
class Tutors (db.Model):

    username = db.StringProperty()
    password = db.StringProperty()
    role = db.StringProperty()