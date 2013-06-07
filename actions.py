from models import Students

class CreateUser(webapp2.RequestHandler):
    def post(self):
        s = Students (name=self.request.get('name'),
                        email=self.request.get('email'),
                        username=self.request.get('username'),
                        password=self.request.get('password'),
                        coursen=self.request.get('courseN'),
                        courset=sef.request.get('courseT'))
        s.put()
    
