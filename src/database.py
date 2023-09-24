# -*- coding: utf-8 -*-

import os
import redis
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
redis_pool = redis.ConnectionPool(
    host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"),
    db=0, max_connections=120)
redis_client = redis.Redis(connection_pool=redis_pool)
