import requests
import json
import time
from datetime import datetime

LOKI_URL = "http://gateway:3100/loki/api/v1/push"
TENANT_ID = "tenant1"
AUTH = ("admin", "admin")

def push_log_to_loki(log_message, level="info"):
    headers = {
        "Content-Type": "application/json",
        "X-Scope-OrgID": TENANT_ID
    }

    log_entry = {
        "streams": [
            {
                "stream": {
                    "level": level,
                    "job": "python-app"
                },
                "values": [
                    [str(int(datetime.now().timestamp() * 1e9)), log_message]
                ]
            }
        ]
    }

    response = requests.post(LOKI_URL, headers=headers, data=json.dumps(log_entry), auth=AUTH)

    if response.status_code == 204:
        print("Log pushed successfully")
    else:
        print(f"Failed to push log: {response.status_code}, {response.text}")

def main():
    while True:
        push_log_to_loki("Something happened", level="info")
        time.sleep(2)

if __name__ == "__main__":
    main()