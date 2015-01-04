from flask import Flask
from models import db
import pkg_resources

VERSION = pkg_resources.require('anovelmous')[0].version

app = Flask(__name__)
app.config.from_envvar("ANOVELMOUS_SETTINGS")
db.init_app(app)

import anovelmous.views
import anovelmous.api