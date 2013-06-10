import webapp2
import cgi
from models import Students

sADMIN_PAGE_HTML = """\
<html>
    <body>
        <form action="" method="post">
            <label for="name">Name</label>:
            <input type="text" name="name" id="name" />
            <br/>
            <label for="email">email</label>:
            <input type="text" name="email" id="email" />
            <br/>
            <label for="username">username</label>:
            <input type="text" name="username" id="username" />
            <br/>
            <label for="password">password</label>:
            <input type="text" name="password" id="password" />
            <br/>
            <label for="courseN">course number</label>:
            <input type="text" name="courseN" id="courseN" />
            <br/>
            <label for="courseT">course type</label>:
            <input type="text" name="courseT" id="courseT" />
            <br/>
            <input type="submit" value=submit />
                
        </form>
    </body>
</html>
"""
LOGIN_PAGE_HTML = """\
                  <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="/css/bootstrap.css" rel="stylesheet" />
    </head>
    <body>
    <div class="container">
        <br/>
        <br/>
        <a class="btn" data-toggle="modal" href="#myModal" role="button">Students &raquo;</a></p>
    <div aria-hidden="true" aria-labelledby="myModalLabel" class="modal hide fade" id="myModal" role="dialog" tabindex="-1">
       <div class="modal-header">
        <button aria-hidden="true" class="close" data-dismiss="modal" type="button">x</button>
        <h3 id="myModalLabel">
         Student Login</h3>
       </div>
       <div class="modal-body">
                    <form action="" method="post">
                        <label for="username">username</label>
                        <input type="text" name="username" id="username" />
                        <br/>
                        <label for="password">password</label>
                        <input type="text" name="password" id="password" />
                        <br/>
                        <input type="submit" value=submit />
                    </form>
       </div>
        <div class="modal-footer">
            <button class="btn" data-dismiss="modal">Close</button></div>
        </div>
     </div>
     </div>
                        <script src="/js/bootstrap.js"></script>
                    <script src="/js/jquery.js"></script>
                    <script src="/js/bootstrap.min.js"></script>
                    </body>
                    </html>
"""

class MainPage(webapp2.RequestHandler):
# Loads the home page

    def get(webapp2):
        webapp2.redirect('h/home.html')
        
class sAdmin(webapp2.RequestHandler):
# Adds entries in Students Entity within the Datastore

    def get(self):
        self.response.write(sADMIN_PAGE_HTML)
    
    def post(self):
        s = Students (name=self.request.get('name'),
                        email=self.request.get('email'),
                        username=self.request.get('username'),
                        password=self.request.get('password'),
                        courseN=self.request.get('courseN'),
                        courseT=self.request.get('courseT'))
        s.put()
        return webapp2.redirect('/')

class Login(webapp2.RequestHandler):
    #launches login modal
    def get(self):  
        self.response.write(LOGIN_PAGE_HTML)
        
    def post(self):
        iName = self.request.get('name')
        iPassword=self.request.get('password')
        
        if  iName == "Phil" :
            return  webapp2.redirect('/' + iName)
        else:
            return webapp2.redirect('/login' + iName)
            
    

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', sAdmin),
    ('/login', Login),
], debug=True)