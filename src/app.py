# -*- coding: utf-8 -*-

import os
import traceback
from flask import Flask
from flask_migrate import Migrate
from database import db, redis_client
from apis.rinha_api import api_rinha_backend_bp

app = Flask(__name__)
app.config.from_pyfile("config.py")

# init flask_sqlalchemy, flask_migrate, flask_redis
db.init_app(app)
migrate = Migrate(app, db)
redis_client.init_app(app)

# register blueprints
app.register_blueprint(api_rinha_backend_bp)
