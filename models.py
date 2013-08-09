from google.appengine.ext import ndb
from webapp2_extras import sessions
from webapp2_extras import auth
from webapp2_extras import security



import webapp2_extras.appengine.auth.models

import logging
import os.path
import webapp2
import time

class User(webapp2_extras.appengine.auth.models.User):
  def set_password(self, raw_password):
    """Sets the password for the current user

    :param raw_password:
        The raw password which will be hashed and stored
    """
    self.password = security.generate_password_hash(raw_password, length=12)

  @classmethod
  def get_by_auth_token(cls, user_id, token, subject='auth'):
    """Returns a user object based on a user ID and token.

    :param user_id:
        The user_id of the requesting user.
    :param token:
        The token string to be verified.
    :returns:
        A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
    """
    token_key = cls.token_model.get_key(user_id, subject, token)
    user_key = ndb.Key(cls, user_id)
    # Use get_multi() to save a RPC call.
    valid_token, user = ndb.get_multi([token_key, user_key])
    if valid_token and user:
        timestamp = int(time.mktime(valid_token.created.timetuple()))
        return user, timestamp
    
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


class RBAC(ndb.Model):

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    courseN = ndb.StringProperty()
    courseT = ndb.StringProperty()
    
class Tutors (ndb.Model):

    username = ndb.StringProperty()
    password = ndb.StringProperty()
    role = ndb.StringProperty()

class Weekend(ndb.Model):
    #Weekend One Program
    wNumber = ndb.TextProperty()
    wDay = ndb.TextProperty()
    slot = ndb.TextProperty()
    outcomes = ndb.TextProperty()
    description = ndb.TextProperty()
    delivery = ndb.TextProperty()
    assessment = ndb.TextProperty()
    resources = ndb.TextProperty()
    duration = ndb.TextProperty()
  
