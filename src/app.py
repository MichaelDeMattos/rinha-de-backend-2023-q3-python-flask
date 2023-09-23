# -*- coding: utf-8 -*-

import os
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("config.py")
