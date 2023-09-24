# -*- coding: utf-8 -*-

import uuid
from database import db
from utils.rinha_util import generate_uuid


class Pessoa(db.Model):
    __tablename__ = "pessoa"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    apelido = db.Column(db.String(32), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    stack = db.Column(db.ARRAY(db.String(32)))
