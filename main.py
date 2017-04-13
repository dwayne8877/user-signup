#Import functions
import webapp2
import re


# Universal header
# Add this to the beginning of all HTML content
page_header = """<html>
    <head>
        <title>User Signup</title>
    </head>
    <body>
"""


# Submission form
# Include %s tokens so that we can pass in parameters later
form = """        <h2>Sign Up</h2>
        <form method="post">
            Username: <input type="text" name="username" value="%s"> <font color="#FF0000">%s</font><br>
            Password: <input type="password" name="password" value=""> <font color="#FF0000">%s</font><br>
            Verify password: <input type="password" name="verify" value=""> <font color="#FF0000">%s</font><br>
            Email (optional): <input type="text" name="email" value="%s"> <font color="#FF0000">%s</font><br>
            <input type="submit">
        </form>
"""


# Universal footer
# Add this to the end of all HTML content
page_footer = """    </body>
</html>"""


# Validate the inputted username using regular expressions
# If the username exists and is of valid form, function returns True
def valid_username(username):
    user_re = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
    return username and user_re.match(username)


# Validate the inputted password
def valid_password(password):
    pass_re = re.compile(r"^.{3,20}$")
    return password and pass_re.match(password)


# Validate the inputted email
def valid_email(email):
    mail_re = re.compile(r"[\S]+@[\S]+.[\S]+$")
    return not email or mail_re.match(email)


# Render page
class MainHandler(webapp2.RequestHandler):
    # get(self) renders the page before any information has been submitted
    def get(self):
        # Build page with empty parameters and display
        # Order of parameters: username, username error, password error, verify error, email, email error
        parameters = ["", "", "", "", "", ""]
        page_content = form % (parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5])
        content = page_header + page_content + page_footer
        self.response.write(content)

    # post(self) only renders after information has been submitted
    def post(self):
        # Initialize variables
        parameters = ["", "", "", "", "", ""]
        error = False

        # Input information
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        # Store username and email if they're present
        if username:
            parameters[0] = username
        if email:
            parameters[4] = email

        # Check if username, password and email are valid and set error value accordingly
        # If errors are present, put error messages in the parameters
        if not valid_username(username):
            parameters[1] = "Error: Invalid username."
            error = True
        if not valid_password(password):
            parameters[2] = "Error: Invalid password."
            error = True
        if not valid_email(email):
            parameters[5] = "Error: invalid email address."
            error = True

        # Only trigger the mismatching passwords error if first password is nonempty
        if password and password != verify:
            parameters[3] = "Error: Passwords do not match."
            error = True

        # If errors are present, rerender the page with accompanying errors
        # Otherwise render the welcome page
        if error:
            page_content = form % (parameters[0], parameters[1], parameters[2], parameters[3], parameters[4], parameters[5])
            content = page_header + page_content + page_footer
            self.response.write(content)
        else:
            page_content = "        <p>Welcome, " + username + "!<p>"
            content = page_header + page_content + page_footer
            self.response.write(content)


# Pair URLs with functions
routes = [("/", MainHandler)]


# Run webapp with debugger enabled
app = webapp2.WSGIApplication(routes, debug=True)
