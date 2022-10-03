
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_migrate import Migrate

from trycourier import Courier


#Initialize Flask app + ensure it works?
app = Flask(__name__)
app.config.from_object('config')


#app.config["DEBUG"] = True

#Configure MySQL connection using SQLALCHEMY:
#SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#    username="jmnguyen1999",
#    password="database",
#    hostname="jmnguyen1999.mysql.pythonanywhere-services.com",
#    databasename="jmnguyen1999$comments"
#    )
#app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

#recycle client connections to this site --> close all connections thats be idle for 299 secs
#app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

#don't use this feature, we don't need it
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#create an instance of SQLAlchemy using the Flask app we just put db configurations into
db = SQLAlchemy(app)

#create an instance of Migrate to hook up the app to the db
migrate = Migrate(app, db)

#set up the login system from flask-login:
app.secret_key= "something only I know sdfleoifsdfkwektvngkhpuo594jf3jsi2ijsdk"
login_manager = LoginManager()
login_manager.init_app(app)

#Models:
#Model User for Flask-Login, its a subclass of UserMixin bc UserMixin is a Flask-Login extension that's very useful
#instances of this User class will be stored in the table it specified
class User(UserMixin, db.Model):
    __tablename__ = "users"

    #create a column/attribute titled this variable name of this type + any other information about this attribute
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(360))
    phone = db.Column(db.String(10))
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.username

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_fname(self):
        return self.fname

    def get_lname(self):
        return self.lname

@login_manager.user_loader
def load_user(user_id):
    #query the "users" db table using our User class, where the "username" column = this given "user.id", and return the first one that matches, returns None if not found
    #returns a User object
    return User.query.filter_by(username=user_id).first()


#Model for SQLAlchemy, For comments from users
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.now) #store an attribute column called "posted", that is a DateTime object, whose default value is the current time the Comment object was created

    #store a way to find the User that posted this comment
    #the foreign key --> will point to the "id" attribute in the "users" db table.
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)

    #to retreive the actual User object found in the users db table based on our foreign key, commenter_id
    commenter = db.relationship('User', foreign_keys=commenter_id)

class SchedNotification(db.Model):
    __tablename__ = "sched_notifications"
    id = db.Column(db.Integer, primary_key = True)
    #store a way to find the User that posted this comment
    #the foreign key --> will point to the "id" attribute in the "users" db table.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    start_time = db.Column(db.DateTime, nullable = False)
    run_method = db.Column(db.String(64), nullable = False)
    message_key = db.Column(db.Integer)
    warning_count = db.Column(db.Integer, default = 0)


    #to retreive the actual User object found in the users db table based on our foreign key, user_id
    user = db.relationship('User', foreign_keys=user_id)

message_keys = {1:"You're X minutes late for work. Come in ASAP.",
2:"You still haven't clocked in 20 min after your shift. We're giving you a write up and will be reconsidering your position here. Come in ASAP.",
3:"You haven't clocked out of your shift yet, please do so ASAP.",
4:"Hey, you still haven't input your availability for time_period, we need it ASAP to generate your next schedule.",
5:"Here's your schedule for time_period:\n\n(some schedule in print or image here)"
}


client = Courier(auth_token="pk_prod_5HSANKGV784BKWG2DW1ZHCV6VA77")

def sendUpdateAvailNotif(fname, time_period, due_date, channels, email = "", phone = ""):
    resp = client.send_message(
      message={
        "to": {
          "email": email,
          "phone_number": phone,
        },
        "template": "A05ZKJHJ2EMQJXNJCE68WD65PN0D",
        "data": {
          "fname": fname,
          "subject_line": "Time for an Availability Update!",
          "time_period": time_period, #"Sunday, 9/11 - Sunday, 9/25",
          "due_date": due_date, #"Saturday, 9/10 @11:59PM PT",
          "channels": channels,
        },
      }
    )

    print(resp['requestId'])

def sendGeneralNotif(message_key, channels, email="", phone="", subject=""):
    resp = client.send_message(
      message={
        "to": {
          "email": email,
          "phone_number": phone,
        },
        "template": "HY861ENK26MFGDNMYWJF9TH1QQ5R",
        "data": {
          "body": message_key,
          "subject_line": subject,
          "channels": channels,
        },
      }
    )

    print(resp['requestId'])

#if on the url for the home page run the following method: index()
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method =="GET":
        #return render_template("main_page.html", comments=Comment.query.all())      #show the page, main_page.html, and pass in the list of Comment objects in the mySQL database to it to display
        return render_template("main_page.html", comments=SchedNotification.query.all())

    #request was a POST request --> create a new Comment object from the user input from main_page.html textbox called "contents", then update into mySQL
    #check user is logged in
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    #------Commenting out old code here-------
    #comment = Comment(content=request.form["contents"], commenter=current_user)
    #db.session.add(comment)
    #db.session.commit()
    #----end commenting old code----

    start = datetime.strptime(request.form["start_time"], '%m/%d/%y %I:%M%p')
    notification = SchedNotification(user = current_user, start_time = start, run_method=request.form["run_method"], message_key=request.form["message_key"], warning_count=request.form["warning_count"])
    db.session.add(notification)
    db.session.commit()

    return redirect(url_for('index'))




#if on the url for the login page run the following method: login()
@app.route("/login/", methods=["GET", "POST"])      #accept GET and POST requests for the clients accessing this url
def login():
    #if client is just reading the page --> display login page for them to enter their login credentials
    if request.method=="GET":
        return render_template("login_page.html", error=False)


    #must have been a POST request --> client submitted credentials --> error check + login if no error:
    #look for an existing instance in the "users" db table that matches the entered username.
    user = load_user(request.form["username"])
    if user is None:
        return render_template("login_page.html", error=True)

    if not user.check_password(request.form["password"]):
        return render_template("login_page.html", error=True)


    # No error reached --> client login and may go to the main page --> calls index()
    login_user(user)
    return redirect(url_for('index'))


#create url to be able to logout!, goes back to home page as an anonymous viewer.
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


'''

Types of notifications needed:
- Email:
    - need update availability/preferences
    - Email next schedule

- Phone:
    - Clock in/out violations, including breaks
    - warnings on updating availability/preferences
    - text next schedule?

Written message bodies:
    - Use General notification template:
        - Clock in violation:
            (5 and 10 min after start shift) You're X minutes late for work. Come in ASAP.
            (20 min after start shift) You still haven't clocked in 20 min after your shift. We're giving you a write up and will be reconsidering your position here. Come in ASAP.

        - Clock out violation:
            (10 min after shift) You haven't clocked out of your shift yet, please do so ASAP.

        - Update Availability Warning:
            (After due date) Hey, you still haven't inputted your availability for time_period, we need it ASAP to generate your next schedule.

        - Next schedule:
            (at scheduled time)
            Here's your schedule for time_period:

            (some schedule in print or image here)

    - Update Availability for Email only --> use specific template


'''

#--------test code for all time task---------------






