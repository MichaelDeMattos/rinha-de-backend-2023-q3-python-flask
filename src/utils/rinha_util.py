# -*- coding: utf-8 -*-

import uuid


def generate_uuid() -> str:
    """ create uuid1 and convert to str """
    return str(uuid.uuid1())
