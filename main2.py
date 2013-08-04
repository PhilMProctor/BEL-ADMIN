#!/usr/bin/env python

from google.appengine.ext import ndb

import jinja2
import logging
import os.path
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from models import wUnit1, User

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'views')
jinja_environment = \
    jinja2.Environment(autoescape=True, extensions=['jinja2.ext.autoescape'], loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

def user_required(handler):
  """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
  """
  def check_login(self, *args, **kwargs):
    auth = self.auth
    if not auth.get_user_by_session():
      self.redirect(self.uri_for('login'), abort=True)
    else:
      return handler(self, *args, **kwargs)

  return check_login

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    """Shortcut to access the auth instance as a property."""
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    """Shortcut to access a subset of the user attributes that are stored
    in the session.

    The list of attributes to store in the session is specified in
      config['webapp2_extras.auth']['user_attributes'].
    :returns
      A dictionary with most user information
    """
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    """Shortcut to access the current logged in user.

    Unlike user_info, it fetches information from the persistence layer and
    returns an instance of the underlying model.

    :returns
      The instance of the user model associated to the logged in user.
    """
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.

    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """    
    return self.auth.store.user_model

  @webapp2.cached_property
  def session(self):
      """Shortcut to access the current session."""
      return self.session_store.get_session(backend="datastore")
    
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

  def display_message(self, message):
    """Utility function to display a template with a simple message."""
    params = {
      'message': message
    }
    self.render_template('message.html', params)

  # this is needed for webapp2 sessions to work
  def dispatch(self):
      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)

      try:
          # Dispatch the request.
          webapp2.RequestHandler.dispatch(self)
      finally:
          # Save all sessions.
          self.session_store.save_sessions(self.response)

class MainHandler(BaseHandler):
  def get(self):
    u = self.user_info
    username = u['name'] if u else None
    params = {'username': username}
    self.render_template('home.html', params)

class SignupHandler(BaseHandler):
  def get(self):
    u = self.user_info
    username = u['name'] if u else None
    params = {'username': username}
    self.render_template('signup.html', params)

  def post(self):
    user_name = self.request.get('username')
    email = self.request.get('email')
    name = self.request.get('name')
    password = self.request.get('password')
    last_name = self.request.get('lastname')

    unique_properties = ['email_address']
    user_data = self.user_model.create_user(user_name,
      unique_properties,
      email_address=email, name=name, password_raw=password,
      last_name=last_name, verified=False)
    if not user_data[0]: #user_data is a tuple
      self.display_message('Unable to create user for email %s because of \
        duplicate keys %s' % (user_name, user_data[1]))
      return
    
    user = user_data[1]
    user_id = user.get_id()

    token = self.user_model.create_signup_token(user_id)

    verification_url = self.uri_for('verification', type='v', user_id=user_id,
      signup_token=token, _full=True)

    msg = 'Send an email to user in order to verify their address. \
          They will be able to do so by visiting <a href="{url}">{url}</a>'

    self.display_message(msg.format(url=verification_url))

class ForgotPasswordHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    username = self.request.get('username')

    user = self.user_model.get_by_auth_id(username)
    if not user:
      logging.info('Could not find any user entry for username %s', username)
      self._serve_page(not_found=True)
      return

    user_id = user.get_id()
    token = self.user_model.create_signup_token(user_id)

    verification_url = self.uri_for('verification', type='p', user_id=user_id,
      signup_token=token, _full=True)

    msg = 'Send an email to user in order to reset their password. \
          They will be able to do so by visiting <a href="{url}">{url}</a>'

    self.display_message(msg.format(url=verification_url))
  
  def _serve_page(self, not_found=False):
    username = self.request.get('username')
    params = {
      'username': username,
      'not_found': not_found
    }
    self.render_template('forgot.html', params)


class VerificationHandler(BaseHandler):
  def get(self, *args, **kwargs):
    user = None
    user_id = kwargs['user_id']
    signup_token = kwargs['signup_token']
    verification_type = kwargs['type']

    # it should be something more concise like
    # self.auth.get_user_by_token(user_id, signup_token
    # unfortunately the auth interface does not (yet) allow to manipulate
    # signup tokens concisely
    user, ts = self.user_model.get_by_auth_token(int(user_id), signup_token,
      'signup')

    if not user:
      logging.info('Could not find any user with id "%s" signup token "%s"',
        user_id, signup_token)
      self.abort(404)
    
    # store user data in the session
    self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)

    if verification_type == 'v':
      # remove signup token, we don't want users to come back with an old link
      self.user_model.delete_signup_token(user.get_id(), signup_token)

      if not user.verified:
        user.verified = True
        user.put()

      self.display_message('User email address has been verified.')
      return
    elif verification_type == 'p':
      # supply user to the page
      params = {
        'user': user,
        'token': signup_token
      }
      self.render_template('resetpassword.html', params)
    else:
      logging.info('verification type not supported')
      self.abort(404)

class SetPasswordHandler(BaseHandler):

  @user_required
  def post(self):
    password = self.request.get('password')
    old_token = self.request.get('t')

    if not password or password != self.request.get('confirm_password'):
      self.display_message('passwords do not match')
      return

    user = self.user
    user.set_password(password)
    user.put()

    # remove signup token, we don't want users to come back with an old link
    self.user_model.delete_signup_token(user.get_id(), old_token)
    
    self.display_message('Password updated')
    
class AdminHandler(BaseHandler):
    @user_required
    def get(self):
      u = self.user_info
      username = u['name']
      params = {
      'username': username
      }
      self.render_template('admin.html', params)
        
class AdminU_Handler(BaseHandler):
    @user_required
    def get(self):
        u = self.user_info
        username = u['name'] if u else None
        params = {'username': username}
        self.render_template('adminU.html', params)

class LoginHandler(BaseHandler):
  def get(self):
    self._serve_page()

  def post(self):
    username = self.request.get('username')
    password = self.request.get('password')
    try:
      u = self.auth.get_user_by_password(username, password, remember=True,
        save_session=True)
      self.redirect(self.uri_for('portal'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', username, type(e))
      self._serve_page(True)

  def _serve_page(self, failed=False):
    username = self.request.get('username')
    params = {
      'username': username,
      'failed': failed
    }
    self.render_template('login.html', params)

class LogoutHandler(BaseHandler):
  def get(self):
    self.auth.unset_session()
    self.redirect(self.uri_for('home'))

class AuthenticatedHandler(BaseHandler):
  @user_required
  def get(self):
    self.render_template('authenticated.html')
    
class PortalHandler(BaseHandler):
  @user_required
  def get(self):
    u = self.user_info
    username = u['name']
    params = {
      'username': username
    }
    self.render_template('portal.html', params)


config = {
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

# Administration
#
class userHandler(BaseHandler):
  #User Admin
  @user_required
  def get(self):
        users = User.query()
        params = {
        'users': users
        }
        self.render_template('users.html', params)


# Start of Work Book Section

# End of Work Book Section
class WorkbookHandler(BaseHandler):
  #Load main workbook page
  @user_required
  def get(self):
        u = self.user_info
        username = u['name']
        params = {
        'username': username
        }
        self.render_template('workbook.html', params)

# Start of Work Book Admin Section

class au1c_Handler(BaseHandler):
    #Give ability to CREATE Unit details
    
    @user_required    
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
        u = self.user_info
        username = u['name']
        params = {
        'username': username
        }
        self.render_template('au1c.html', params)
        
class au1v_Handler(BaseHandler):
    #Give ability to VIEW Unit details
    @user_required
    def get(self):
        u = self.user_info
        username = u['name']
        unitNo = wUnit1.query(wUnit1.ftype == "Template")
        params = {
        'unitNo' : unitNo,
        'username': username
        }
        self.render_template('au1v.html', params)
        
        
class au1e_Handler(BaseHandler):
    #Give ability to EDIT Unit details
    @user_required 
    def post(self):
        u = self.user_info
        author = u['name']

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
        u = self.user_info
        username = u['name']
        unitNo = wUnit1.query(wUnit1.ftype == "Template")
        params = {
        'unitNo' : unitNo,
        'username': username
        }
        self.render_template('au1e.html', params)
        
class u1Handler(BaseHandler):
  #Load main workbook page
  @user_required
  def get(self):
        u = self.user_info
        username = u['name']
        params = {
        'username': username
        }
        self.render_template('u1.html', params)
        
# End of Work Book Admin Section

application = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name='home'),
    webapp2.Route('/signup', SignupHandler),
    webapp2.Route('/<type:v|p>/<user_id:\d+>-<signup_token:.+>',
      handler=VerificationHandler, name='verification'),
    webapp2.Route('/password', SetPasswordHandler),
    webapp2.Route('/login', LoginHandler, name='login'),
    webapp2.Route('/portal', PortalHandler, name='portal'),
    webapp2.Route('/admin', AdminHandler, name="admin"),
    webapp2.Route('/adminU', AdminU_Handler, name="adminU"),
    webapp2.Route('/logout', LogoutHandler, name='logout'),
    webapp2.Route('/forgot', ForgotPasswordHandler, name='forgot'),
    webapp2.Route('/authenticated', AuthenticatedHandler, name='authenticated'),
    webapp2.Route('/workbook', WorkbookHandler, name='workbook'),
    webapp2.Route ('/au1c', au1c_Handler, name='au1c'),
    webapp2.Route ('/au1e', au1e_Handler, name='au1e'),
    webapp2.Route ('/au1v', au1v_Handler, name='au1v'),
    webapp2.Route ('/u1', u1_Handler, name='u1'),
    webapp2.Route ('/users', userHandler, name='uAdmin')
], debug=True, config=config)

logging.getLogger().setLevel(logging.DEBUG)
