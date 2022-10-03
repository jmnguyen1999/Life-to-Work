
from time import sleep
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ENGINE_OPTIONS
from flask_app import SchedNotification, User
from datetime import datetime
import pytz


from trycourier import Courier


engine = create_engine(
    SQLALCHEMY_DATABASE_URI, **SQLALCHEMY_ENGINE_OPTIONS
)
Session = sessionmaker(engine)



#--------------------------Methods and constants to run while "processing jobs" in the db table------------------------
message_keys = {
    "1":"You're X minutes late for work. Come in ASAP.",
    "2":"You still haven't clocked in 20 min after your shift. We're giving you a write up and will be reconsidering your position here. Come in ASAP.",
    "3":"You haven't clocked out of your shift yet, please do so ASAP.",
    "4":"Hey, you still haven't input your availability for time_period, we need it ASAP to generate your next schedule.",
    "5":"Here's your schedule for time_period:\n\n(some schedule in print or image here)"
    }

def sendUpdateAvailNotif(fname, time_period, due_date, channels, email = "", phone = ""):
    print("in sendUpdateAvailNotif():")
    
    client = Courier(auth_token="pk_prod_5HSANKGV784BKWG2DW1ZHCV6VA77")
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

    print("sendUpdateAvailNotif():  Done sending    ", resp['requestId'])

def sendGeneralNotif(message_key, channels, email="", phone="", subject=""):
    print("in sendGeneralNotif():")
    
    client = Courier(auth_token="pk_prod_5HSANKGV784BKWG2DW1ZHCV6VA77")
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

    print("sendGeneralNotif():  Done sending    ", resp['requestId'])
    
#query for first SchedNotification that 
def find_job():
    print("in find_job():", flush=True)
    #present = datetime.now()
    #dt_string = present.strftime("%A, %B %d %Y at %I:%M%p")
    #print("in find_job(): present=", dt_string)

    present_us_pacific = datetime.now(pytz.timezone('America/Los_Angeles'))
    print("US Pacific Current DateTime:", present_us_pacific.strftime("%A, %B %d %Y at %I:%M%p"))
    
    # extract components
    print('TimeZone Name:', present_us_pacific.tzname())
    print('UTC offset:', present_us_pacific.utcoffset())

    with Session.begin() as session:
        #queue = session.query(SchedNotification).filter(SchedNotification.start_time < present).order_by(SchedNotification.start_time)
        notifs = session.query(SchedNotification).filter(SchedNotification.start_time < present_us_pacific).order_by(SchedNotification.start_time)
      
        if notifs is not None:
            #for row in notifs:
            #    print ("start_time:",row.start_time.strftime("%A, %B %d %Y at %I:%M%p"), "Id: ",row.id, "method_name:",row.run_method, "user:",row.user.username)
            if row := notifs.first():
                print ("Id: ",row.id, "start_time:",row.start_time.strftime("%A, %B %d %Y at %I:%M%p"), "method_name:",row.run_method, "message_key:",row.message_key)
            
                #session.query(SchedNotification).filter_by(id=row.id).delete()
                #session.commit()
            
                return notifs

#Given all SchedNotif objects to be processed, call the appropriate method + message_keys for each
def process_jobs(notifs):
    print("in process_job()")
    
    #for every notif --> call appropriate method + delete the row:
    for notif in notifs:
        method = notif.run_method
        print("process_job():  method = ", method)
            
        if method == "sendUpdateAvailNotif":
            user = notif.user
                
            #hardcoded for now, will include in user account in some way in db later
            time_period = "Sunday, 9/11 - Sunday, 9/25"
            due_date = "Saturday, 9/10 @11:59PM PT"
            channels = ["email"]
                
            sendUpdateAvailNotif(user.fname, time_period, due_date, channels, user.email, user.phone)
                
        if method == "sendGeneralNotif": 
            #for reference  -------> sendGeneralNotif(message_key, channels, email="", phone="", subject=""):
            channels = ["phone"]
            sendGeneralNotif(message_keys[notif.message_key], channels, notif.user.email, notif.user.phone)
            
            
        with Session.begin() as session:
            session.query(SchedNotification).filter_by(id=notif.id).delete()
            session.commit()
            
            #    session.query(Job).filter_by(slug=slug).update(
            #        {"result": result, "state": "completed"}
            #    )
            #User.query.filter(User.id == 123).delete()
            #obj = User.query.filter_by(id=123).one()
            #session.delete(obj)
        
        
    print("process_job():  finished, all notifs should be deleted in db by now.")


if __name__ == "__main__":
    while True:
        if jobs := find_job():
            process_jobs(jobs)
            print("done processing job, sleeping for 30 sec before looking for another")
            sleep(30)
        else:
            print("find_job() didn't return anything, sleeping for 30 sec before trying it again.")
            sleep(30)
