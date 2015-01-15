from flask import Flask
from models import db
import os

app = Flask(__name__)
app.config['DEBUG'] = os.environ.get('DEBUG', False)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('ANOVELMOUS_SECRET_KEY', 'development')
db.init_app(app)

import anovelmous.views
import anovelmous.api