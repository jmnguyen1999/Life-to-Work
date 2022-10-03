from getpass import getuser


# Database setup
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="jmnguyen1999",
    password="database",
    hostname="jmnguyen1999.mysql.pythonanywhere-services.com",
    databasename="jmnguyen1999$comments"
    )
SQLALCHEMY_ENGINE_OPTIONS = {"pool_recycle": 299}
SQLALCHEMY_TRACK_MODIFICATIONS = False



