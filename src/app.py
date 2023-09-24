# -*- coding: utf-8 -*-

import os
import traceback
from flask import Flask
from flask_migrate import Migrate
from database import db
from apis.rinha_api import api_rinha_backend_bp

app = Flask(__name__)
app.config.from_pyfile("config.py")

# init flask_sqlalchemy and flask_migrate
db.init_app(app)
migrate = Migrate(app, db)

# register blueprints
app.register_blueprint(api_rinha_backend_bp)
