from flask import Flask
from flask_cors import CORS
from flask_heroku import Heroku
import os

#For persistent storage
from flask_sqlalchemy import SQLAlchemy

#create the Flask app
app = Flask(__name__)
CORS(app)
 
if "TESTING" in os.environ:
    app.config.from_envvar('TESTING')
    print("Using config for TESTING")
elif "DEVELOPMENT" in os.environ:
    app.config.from_envvar('DEVELOPMENT')
    print("Using config for DEVELOPMENT")
else:
    app.config.from_pyfile('config_dply.cfg')
    print("Using config for deployment")

# instantiate the Heroku object before db
heroku = Heroku(app)

# instantiate SQLAlchemy to handle db process
db = SQLAlchemy(app)

#run the file routes.py
from application import routes
