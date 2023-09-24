# -*- coding: utf-8 -*-

import os
import sys
import uuid
import traceback
import subprocess

app_path = os.path.dirname(os.path.abspath(__file__))

try:
    if not os.path.isdir(os.path.join(app_path,  "migrations")):
        subprocess.call("python -m flask db init", shell=True)
        subprocess.call(
            f"python -m flask db migrate -m '{str(uuid.uuid1())}'", shell=True)
        subprocess.call("python -m flask db upgrade head", shell=True)
    update_model = subprocess.run(
        "python -m flask db check", shell=True, capture_output=True, text=True)
    if "No new upgrade operations detected" in update_model.stdout:
        print("Flask-Migrate: No new upgrade operations detected", flush=True)
    else:
        subprocess.call(
            f"python -m flask db migrate -m '{str(uuid.uuid1())}'", shell=True)
        subprocess.call("python -m flask db upgrade head", shell=True)
except Exception:
    traceback.print_exc()
finally:
    _, uwsgi_instance = sys.argv
    if os.getenv("DEV_MODE") == "true":
        subprocess.call(f"python -m pytest tests", shell=True)
        subprocess.call(
            f"uwsgi --ini {uwsgi_instance} --py-autoreload 1", shell=True)
    else:
        subprocess.call(
            f"uwsgi --ini {uwsgi_instance}", shell=True)
