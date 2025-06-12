# app/services/maersk_client.py

import requests
import os
from typing import Optional

class MaerskAPIClient:
    def __init__(self):
        self.client_id = os.getenv("MAERSK_CLIENT_ID")
        self.client_secret = os.getenv("MAERSK_CLIENT_SECRET")
        self.token_url = os.getenv("MAERSK_TOKEN_URL")
        self.track_url = os.getenv("MAERSK_TRACK_URL")  # base URL like https://api.maersk.com/track-and-trace/containers
        self.token: Optional[str] = None

    def authenticate(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.token_url, data=payload, headers=headers)
        response.raise_for_status()
        self.token = response.json().get("access_token")

    def track_container(self, container_id: str):
        if not self.token:
            self.authenticate()
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.track_url}/{container_id}", headers=headers)
        response.raise_for_status()
        return response.json()
