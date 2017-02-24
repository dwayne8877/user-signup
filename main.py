import webapp2
import re


def build_page():

    header= "<h1 align='center'>User Signup</h1>"

    username_label ="<label> Username: </label>"
    username_input = "<input name='username' value='%(username)s'/>"

    password_label = "<label> Password: </label>"
    password_input = "<input type = 'password' name = 'password' value='%(password)s'/>"

    verify_label = "<label> Verify Password: </label>"
    verify_input = "<input type = 'password' name = 'verify_password' value='%(verify_password)s'/>"

    email_label = "<label> Email (optional): </label>"
    email_input = "<input name = 'email' value='%(email)s' />"

    submit = "<input type='submit' />"


    form = ("<form align='center' method='post'>"

            + username_label + username_input + "<label style = 'color:red' ></label>" +
            "<br>"
            + password_label + password_input + "<label style = 'color:red' > </label>" +
            "<br>"
            + verify_label + verify_input + "<label style = 'color:red' > </label>" +
            "<br>"
            + email_label + email_input + "<label style = 'color:red' >  </label>"
            "<br>"

            + "<div style ='color: red' > %(error)s </div>"
            + submit +
            "</form>")

    return header + form


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):

    def write_form(self, error="", username="", password="", verify_password="", email=""):

        content = build_page()

        self.response.out.write(content % {"error": error,
                                            "username": username,
                                            "password": password,
                                            "verify_password": verify_password,
                                            "email": email})

    def get(self):
        self.write_form()


    def post(self):

        username = self.request.get('username')
        password = self.request.get('password')
        verify_password = self.request.get('verify_password')
        email = self.request.get('email')

        username2 = valid_username(username)
        password2 = valid_password(password)
        verify_password2 = valid_password(verify_password)
        email2 = valid_email(email)

        if not (username2 and password2 and verify_password2 and email2):
            #self.response.out.write(content)
            #self.write_form('Please resubmit information', 'Invalid Username',
            #'Invalid Password',"Your Passwords don't match",'Invalid Email' )
            self.write_form ('Please resubmit',username,password, verify_password2
                            email)

        #if not (password2 and verify_password2):
            #self.write_form('', '','Your passwords dont match')

        #if not (email2):
            #self.write_form('','','','Invalid email')
        else:
            self.response.write('Thank You!')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
