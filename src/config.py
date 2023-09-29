# -*- coding: utf-8 -*-

import os

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_URI")
SQLALCHEMY_POOL_SIZE = 100
REDIS_URL = os.getenv("REDIS_URL")
