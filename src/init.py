# -*- coding: utf-8 -*-

import os
import sys
import uuid
import traceback
import subprocess

app_path = os.path.dirname(os.path.abspath(__file__))

try:
    _, instance = sys.argv
    if not os.path.isdir(os.path.join(app_path,  "migrations")):
        if "5000" in instance: # create initial migration on first instance
            subprocess.call("python -m flask db init", shell=True)
            subprocess.call(
                f"python -m flask db migrate -m '{str(uuid.uuid1())}'",
                shell=True)
            subprocess.call("python -m flask db upgrade head", shell=True)
    if "5000" in instance: # run migrations on first instance
        update_model = subprocess.run(
            "python -m flask db check", shell=True, capture_output=True,
            text=True)
        if "No new upgrade operations detected" in update_model.stdout:
            print("Flask-Migrate: No new upgrade operations detected",
                  flush=True)
        else:
            subprocess.call(
                f"python -m flask db migrate -m '{str(uuid.uuid1())}'",
                shell=True)
            subprocess.call("python -m flask db upgrade head", shell=True)
except Exception:
    traceback.print_exc()
finally:
    if os.getenv("DEV_MODE") == "true":
        if "5000" in instance: # run tests on first instance
            subprocess.call(f"python -m pytest tests", shell=True)
        subprocess.call(
            f"python -m flask run -h {instance.split(':')[0]}" \
            f" -p {instance.split(':')[1]} --debug",
            shell=True)
    else:
        subprocess.call(
            f"python -m gunicorn "
            f"--workers 3 "
            f"--worker-class gevent "
            f"--worker-connections 1000 "
            f"--bind {instance} "
            f"app:app",
            shell=True)
