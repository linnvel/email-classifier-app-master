import os
from flask import Flask
from flask_mysqldb import MySQL
from datetime import timedelta
from flask_mail import Mail


# Config Web app
app = Flask(__name__)
app.secret_key = 'secret123'
# make session expire if no activities in 2 minutes
app.permanent_session_lifetime = timedelta(minutes=2)

# Init MYSQL
mysql = MySQL(app)

# Config MySQL
app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'emailclassifier'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Config mail
# you can change to your own email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
#app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'sherry.chen012@gmail.com'#os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = 'zjtuavuwqarmkjzc'#os.environ.get('EMAIL_PASS')
mail = Mail(app)

from app import views
