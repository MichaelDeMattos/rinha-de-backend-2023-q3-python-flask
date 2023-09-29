# -*- coding: utf-8 -*-

import uuid
from datetime import datetime


def generate_uuid() -> str:
    """ create uuid1 and convert to str """
    return str(uuid.uuid1())

def date_is_valid(date: str) -> bool:
    """ Check if date string is valid to convert to date object """
    year, month, day = date.split("-")
    try:
        datetime(year=int(year), month=int(month), day=int(day))
        return True
    except Exception:
        return False

def stack_is_valid(stack: object) -> bool:
    """ Check if stack list is valid to insert in database """
    try:
        if not stack:
            return True
        if isinstance(stack, (tuple, dict, str)):
            return False
        if isinstance(stack, list):
            is_valid = True
            for element in stack:
                if not isinstance(element, str):
                    is_valid = False
                    break
            if is_valid:
                return True
            else:
                False
    except Exception:
        return False
