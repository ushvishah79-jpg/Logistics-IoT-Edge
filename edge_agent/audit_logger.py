import json
import os
from datetime import datetime

HISTORY_FILE = "update_history.json"


def initialize_history():

    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as f:

            json.dump([], f, indent=4)


def save_history(
    version,
    build_number,
    status,
    message=""
):

    initialize_history()

    with open(HISTORY_FILE, "r") as f:

        history = json.load(f)

    history.append({

        "timestamp": datetime.now().isoformat(),

        "version": version,

        "build_number": build_number,

        "status": status,

        "message": message

    })

    with open(HISTORY_FILE, "w") as f:

        json.dump(history, f, indent=4)


def get_history():

    initialize_history()

    with open(HISTORY_FILE, "r") as f:

        return json.load(f)