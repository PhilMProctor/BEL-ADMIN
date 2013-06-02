import webapp2


class MainPage(webapp2.RequestHandler):

    def get(webapp2):
        webapp2.redirect('templates/home.html')


application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)