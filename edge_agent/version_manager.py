import json
import os
from datetime import datetime

VERSION_FILE = "installed_version.json"


def initialize():
    if not os.path.exists(VERSION_FILE):
        data = {
            "version": "0.0.0",
            "build_number": 0,
            "installed_at": ""
        }

        with open(VERSION_FILE, "w") as f:
            json.dump(data, f, indent=4)


def get_current_version():

    initialize()

    with open(VERSION_FILE, "r") as f:
        return json.load(f)


def get_current_build():

    data = get_current_version()

    return data["build_number"]


def save_version(version, build_number):

    data = {
        "version": version,
        "build_number": build_number,
        "installed_at": datetime.now().isoformat()
    }

    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=4)


def is_rollback(incoming_build):

    current_build = get_current_build()

    return incoming_build <= current_build